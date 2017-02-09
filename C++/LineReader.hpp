#ifndef CSV_PARSER_H
#define CSV_PARSER_H

#include <cstring>
#include <cstdio>
#include <exception>
#include <cassert>
#ifndef CSV_IO_NO_THREAD
#include <future>
#endif

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
                errno = 0;
            }

            void set_errno(int errno_value){
                this->errno_value = errno_value;
            }

            int errno_value;
        };

        struct can_not_open_file : base, with_file_name, with_errno{
            void format_error_message()const{
                if(errno_value != 0)
                    std::snprintf(error_message_buffer, sizeof(error_message_buffer),
                    "Can not open file \"%s\" because \"%s\".", file_name, std::strerror(errno_value));
                else
                    std::snprintf(error_message_buffer, sizeof(error_message_buffer),
                    "Can not open file \"%s\"." , file_name);
            }
        };

        struct line_length_limit_exceeded : base, with_file_name, with_file_line{
            void format_error_message()const{
                std::snprintf(error_message_buffer, sizeof(error_message_buffer),
                "Line number %d in file \"%s\" exceeds the maximum length of 2^24-1.", file_line, file_name);
            }
        };
    }

    class LineReader{
    private:
        static const int block_len = 1<<24;
        #ifndef CSV_IO_NO_THREAD
        std::future<int>bytes_read;
        #endif
        FILE*file;
        char*buffer;
        int data_begin;
        int data_end;

        char file_name[error::max_file_name_length+1];
        unsigned file_line;

        void open_file(const char*file_name){
            // We open the file in binary mode as it makes no difference under *nix
            // and under Windows we handle \r\n newlines ourself.
            file = std::fopen(file_name, "rb");
            if(file == 0){
                int x = errno; // store errno as soon as possible, doing it after constructor call can fail.
                error::can_not_open_file err;
                err.set_errno(x);
                err.set_file_name(file_name);
                throw err;
            }
        }

        void init(){
            file_line = 0;

            // Tell the std library that we want to do the buffering ourself.
            std::setvbuf(file, 0, _IONBF, 0);

            try{
                buffer = new char[3*block_len];
            }catch(...){
                std::fclose(file);
                throw;
            }

            data_begin = 0;
            data_end = std::fread(buffer, 1, 2*block_len, file);

            // Ignore UTF-8 BOM
            if(data_end >= 3 && buffer[0] == '\xEF' && buffer[1] == '\xBB' && buffer[2] == '\xBF'){
                data_begin = 3;
            }

            #ifndef CSV_IO_NO_THREAD
            if(data_end == 2*block_len){
                bytes_read = std::async(std::launch::async, [=]()->int{
                    return std::fread(buffer + 2*block_len, 1, block_len, file);
                });
            }
            #endif
        }

    public:
        LineReader() = delete;
        LineReader(const LineReader&) = delete;
        LineReader&operator=(const LineReader&) = delete;

        LineReader(const char*file_name, FILE*file):
        file(file){
            set_file_name(file_name);
            init();
        }

        LineReader(const std::string&file_name, FILE*file):
        file(file){
            set_file_name(file_name.c_str());
            init();
        }

        explicit LineReader(const char*file_name){
            set_file_name(file_name);
            open_file(file_name);
            init();
        }

        explicit LineReader(const std::string&file_name){
            set_file_name(file_name.c_str());
            open_file(file_name.c_str());
            init();
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
                #ifndef CSV_IO_NO_THREAD
                if(bytes_read.valid())
                #endif
                {
                    #ifndef CSV_IO_NO_THREAD
                    data_end += bytes_read.get();
                    #else
                    data_end += std::fread(buffer + 2*block_len, 1, block_len, file);
                    #endif
                    std::memcpy(buffer+block_len, buffer+2*block_len, block_len);

                    #ifndef CSV_IO_NO_THREAD
                    bytes_read = std::async(std::launch::async, [=]()->int{
                        return std::fread(buffer + 2*block_len, 1, block_len, file);
                    });
                    #endif
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
            if(line_end != data_begin && buffer[line_end-1] == '\r'){
                buffer[line_end-1] = '\0';
            }

            char*ret = buffer + data_begin;
            data_begin = line_end+1;
            return ret;
        }

        ~LineReader(){
            #ifndef CSV_IO_NO_THREAD
            // GCC needs this or it will crash.
            if(bytes_read.valid()){
                bytes_read.get();
            }
            #endif

            delete[] buffer;
            std::fclose(file);
        }
    };
}
#endif
