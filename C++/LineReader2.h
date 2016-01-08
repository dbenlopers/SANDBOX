#ifndef CSV_H
#define CSV_H

#include <vector>
#include <string>
#include <cstring>
#include <algorithm>
#include <utility>
#include <cstdio>
#include <exception>
#ifndef CSV_IO_NO_THREAD
#include <mutex>
#include <thread>
#include <condition_variable>
#endif
#include <memory>
#include <cassert>
#include <cerrno>
#include <istream>

namespace io{
    namespace error{
            struct base : std::exception{
                    virtual void format_error_message()const = 0;

                    const char*what()const throw(){
                            format_error_message();
                            return error_message_buffer;
                    }

                    mutable char error_message_buffer[256];
            };

            const int max_file_name_length = 255;

            struct with_file_name{
                    with_file_name(){
                            std::memset(file_name, 0, max_file_name_length+1);
                    }

                    void set_file_name(const char*file_name){
                            std::strncpy(this->file_name, file_name, max_file_name_length);
                            this->file_name[max_file_name_length] = '\0';
                    }

                    char file_name[max_file_name_length+1];
            };

            struct with_file_line{
                    with_file_line(){
                            file_line = -1;
                    }

                    void set_file_line(int file_line){
                            this->file_line = file_line;
                    }

                    int file_line;
            };

            struct with_errno{
                    with_errno(){
                            errno_value = 0;
                    }

                    void set_errno(int errno_value){
                            this->errno_value = errno_value;
                    }

                    int errno_value;
            };

            struct can_not_open_file :
                    base,
                    with_file_name,
                    with_errno{
                    void format_error_message()const{
                            if(errno_value != 0)
                                    std::snprintf(error_message_buffer, sizeof(error_message_buffer),
                                            "Can not open file \"%s\" because \"%s\"."
                                            , file_name, std::strerror(errno_value));
                            else
                                    std::snprintf(error_message_buffer, sizeof(error_message_buffer),
                                            "Can not open file \"%s\"."
                                            , file_name);
                    }
            };

            struct line_length_limit_exceeded :
                    base,
                    with_file_name,
                    with_file_line{
                    void format_error_message()const{
                            std::snprintf(error_message_buffer, sizeof(error_message_buffer),
                                    "Line number %d in file \"%s\" exceeds the maximum length of 2^24-1."
                                    , file_line, file_name);
                    }
            };
    }

    class ByteSourceBase{
    public:
            virtual int read(char*buffer, int size)=0;
            virtual ~ByteSourceBase(){}
    };

    namespace detail{

            class OwningStdIOByteSourceBase : public ByteSourceBase{
            public:
                    explicit OwningStdIOByteSourceBase(FILE*file):file(file){
                            // Tell the std library that we want to do the buffering ourself.
                            std::setvbuf(file, 0, _IONBF, 0);
                    }

                    int read(char*buffer, int size){
                            return std::fread(buffer, 1, size, file);
                    }

                    ~OwningStdIOByteSourceBase(){
                            std::fclose(file);
                    }

            private:
                    FILE*file;
            };

            class NonOwningIStreamByteSource : public ByteSourceBase{
            public:
                    explicit NonOwningIStreamByteSource(std::istream&in):in(in){}

                    int read(char*buffer, int size){
                            in.read(buffer, size);
                            return in.gcount();
                    }

                    ~NonOwningIStreamByteSource(){}

            private:
                   std::istream&in;
            };

            class NonOwningStringByteSource : public ByteSourceBase{
            public:
                    NonOwningStringByteSource(const char*str, long long size):str(str), remaining_byte_count(size){}

                    int read(char*buffer, int desired_byte_count){
                            int to_copy_byte_count = desired_byte_count;
                            if(remaining_byte_count < to_copy_byte_count)
                                    to_copy_byte_count = remaining_byte_count;
                            std::memcpy(buffer, str, to_copy_byte_count);
                            remaining_byte_count -= to_copy_byte_count;
                            str += to_copy_byte_count;
                            return to_copy_byte_count;
                    }

                    ~NonOwningStringByteSource(){}

            private:
                    const char*str;
                    long long remaining_byte_count;
            };

            #ifndef CSV_IO_NO_THREAD
            class AsynchronousReader{
            public:
                    void init(std::unique_ptr<ByteSourceBase>arg_byte_source){
                            std::unique_lock<std::mutex>guard(lock);
                            byte_source = std::move(arg_byte_source);
                            desired_byte_count = -1;
                            termination_requested = false;
                            worker = std::thread(
                                    [&]{
                                            std::unique_lock<std::mutex>guard(lock);
                                            try{
                                                    for(;;){
                                                            read_requested_condition.wait(
                                                                    guard,
                                                                    [&]{
                                                                            return desired_byte_count != -1 || termination_requested;
                                                                    }
                                                            );
                                                            if(termination_requested)
                                                                    return;

                                                            read_byte_count = byte_source->read(buffer, desired_byte_count);
                                                            desired_byte_count = -1;
                                                            if(read_byte_count == 0)
                                                                    break;
                                                            read_finished_condition.notify_one();
                                                    }
                                            }catch(...){
                                                    read_error = std::current_exception();
                                            }
                                            read_finished_condition.notify_one();
                                    }
                            );
                    }

                    bool is_valid()const{
                            return byte_source != 0;
                    }

                    void start_read(char*arg_buffer, int arg_desired_byte_count){
                            std::unique_lock<std::mutex>guard(lock);
                            buffer = arg_buffer;
                            desired_byte_count = arg_desired_byte_count;
                            read_byte_count = -1;
                            read_requested_condition.notify_one();
                    }

                    int finish_read(){
                            std::unique_lock<std::mutex>guard(lock);
                            read_finished_condition.wait(
                                    guard,
                                    [&]{
                                            return read_byte_count != -1 || read_error;
                                    }
                            );
                            if(read_error)
                                    std::rethrow_exception(read_error);
                            else
                                    return read_byte_count;
                    }

                    ~AsynchronousReader(){
                            if(byte_source != 0){
                                    {
                                            std::unique_lock<std::mutex>guard(lock);
                                            termination_requested = true;
                                    }
                                    read_requested_condition.notify_one();
                                    worker.join();
                            }
                    }

            private:
                    std::unique_ptr<ByteSourceBase>byte_source;

                    std::thread worker;

                    bool termination_requested;
                    std::exception_ptr read_error;
                    char*buffer;
                    int desired_byte_count;
                    int read_byte_count;

                    std::mutex lock;
                    std::condition_variable read_finished_condition;
                    std::condition_variable read_requested_condition;
            };
            #endif

            class SynchronousReader{
            public:
                    void init(std::unique_ptr<ByteSourceBase>arg_byte_source){
                            byte_source = std::move(arg_byte_source);
                    }

                    bool is_valid()const{
                            return byte_source != 0;
                    }

                    void start_read(char*arg_buffer, int arg_desired_byte_count){
                            buffer = arg_buffer;
                            desired_byte_count = arg_desired_byte_count;
                    }

                    int finish_read(){
                            return byte_source->read(buffer, desired_byte_count);
                    }
            private:
                    std::unique_ptr<ByteSourceBase>byte_source;
                    char*buffer;
                    int desired_byte_count;
            };
    }

    class LineReader{
    private:
            static const int block_len = 1<<24;
            #ifdef CSV_IO_NO_THREAD
            detail::SynchronousReader reader;
            #else
            detail::AsynchronousReader reader;
            #endif
            char*buffer;
            int data_begin;
            int data_end;

            char file_name[error::max_file_name_length+1];
            unsigned file_line;

            static std::unique_ptr<ByteSourceBase> open_file(const char*file_name){
                    // We open the file in binary mode as it makes no difference under *nix
                    // and under Windows we handle \r\n newlines ourself.
                    FILE*file = std::fopen(file_name, "rb");
                    if(file == 0){
                            int x = errno; // store errno as soon as possible, doing it after constructor call can fail.
                            error::can_not_open_file err;
                            err.set_errno(x);
                            err.set_file_name(file_name);
                            throw err;
                    }
                    return std::unique_ptr<ByteSourceBase>(new detail::OwningStdIOByteSourceBase(file));
            }

            void init(std::unique_ptr<ByteSourceBase>byte_source){
                    file_line = 0;

                    buffer = new char[3*block_len];
                    try{
                            data_begin = 0;
                            data_end = byte_source->read(buffer, 2*block_len);

                            // Ignore UTF-8 BOM
                            if(data_end >= 3 && buffer[0] == '\xEF' && buffer[1] == '\xBB' && buffer[2] == '\xBF')
                                    data_begin = 3;

                            if(data_end == 2*block_len){
                                    reader.init(std::move(byte_source));
                                    reader.start_read(buffer + 2*block_len, block_len);
                            }
                    }catch(...){
                            delete[]buffer;
                            throw;
                    }
            }

    public:
            LineReader() = delete;
            LineReader(const LineReader&) = delete;
            LineReader&operator=(const LineReader&) = delete;

            explicit LineReader(const char*file_name){
                    set_file_name(file_name);
                    init(open_file(file_name));
            }

            explicit LineReader(const std::string&file_name){
                    set_file_name(file_name.c_str());
                    init(open_file(file_name.c_str()));
            }

            LineReader(const char*file_name, std::unique_ptr<ByteSourceBase>byte_source){
                    set_file_name(file_name);
                    init(std::move(byte_source));
            }

            LineReader(const std::string&file_name, std::unique_ptr<ByteSourceBase>byte_source){
                    set_file_name(file_name.c_str());
                    init(std::move(byte_source));
            }

            LineReader(const char*file_name, const char*data_begin, const char*data_end){
                    set_file_name(file_name);
                    init(std::unique_ptr<ByteSourceBase>(new detail::NonOwningStringByteSource(data_begin, data_end-data_begin)));
            }

            LineReader(const std::string&file_name, const char*data_begin, const char*data_end){
                    set_file_name(file_name.c_str());
                    init(std::unique_ptr<ByteSourceBase>(new detail::NonOwningStringByteSource(data_begin, data_end-data_begin)));
            }

            LineReader(const char*file_name, FILE*file){
                    set_file_name(file_name);
                    init(std::unique_ptr<ByteSourceBase>(new detail::OwningStdIOByteSourceBase(file)));
            }

            LineReader(const std::string&file_name, FILE*file){
                    set_file_name(file_name.c_str());
                    init(std::unique_ptr<ByteSourceBase>(new detail::OwningStdIOByteSourceBase(file)));
            }

            LineReader(const char*file_name, std::istream&in){
                    set_file_name(file_name);
                    init(std::unique_ptr<ByteSourceBase>(new detail::NonOwningIStreamByteSource(in)));
            }

            LineReader(const std::string&file_name, std::istream&in){
                    set_file_name(file_name.c_str());
                    init(std::unique_ptr<ByteSourceBase>(new detail::NonOwningIStreamByteSource(in)));
            }

            void set_file_name(const std::string&file_name){
                    set_file_name(file_name.c_str());
            }

            void set_file_name(const char*file_name){
                    strncpy(this->file_name, file_name, error::max_file_name_length);
                    this->file_name[error::max_file_name_length] = '\0';
            }

            const char*get_truncated_file_name()const{
                    return file_name;
            }

            void set_file_line(unsigned file_line){
                    this->file_line = file_line;
            }

            unsigned get_file_line()const{
                    return file_line;
            }

            char*next_line(){
                    if(data_begin == data_end)
                            return 0;

                    ++file_line;

                    assert(data_begin < data_end);
                    assert(data_end <= block_len*2);

                    if(data_begin >= block_len){
                            std::memcpy(buffer, buffer+block_len, block_len);
                            data_begin -= block_len;
                            data_end -= block_len;
                            if(reader.is_valid())
                            {
                                    data_end += reader.finish_read();
                                    std::memcpy(buffer+block_len, buffer+2*block_len, block_len);
                                    reader.start_read(buffer + 2*block_len, block_len);
                            }
                    }

                    int line_end = data_begin;
                    while(buffer[line_end] != '\n' && line_end != data_end){
                            ++line_end;
                    }

                    if(line_end - data_begin + 1 > block_len){
                            error::line_length_limit_exceeded err;
                            err.set_file_name(file_name);
                            err.set_file_line(file_line);
                            throw err;
                    }

                    if(buffer[line_end] == '\n'){
                            buffer[line_end] = '\0';
                    }else{
                            // some files are missing the newline at the end of the
                            // last line
                            ++data_end;
                            buffer[line_end] = '\0';
                    }

                    // handle windows \r\n-line breaks
                    if(line_end != data_begin && buffer[line_end-1] == '\r')
                            buffer[line_end-1] = '\0';

                    char*ret = buffer + data_begin;
                    data_begin = line_end+1;
                    return ret;
            }

            ~LineReader(){
                    delete[] buffer;
            }
    };
}
#endif
