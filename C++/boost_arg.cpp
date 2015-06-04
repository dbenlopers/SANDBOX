/* 
 * Play with boost fileUNDER HEAVY DEVELOPPEMENT
 */
#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

namespace
{
	const size_t ERROR_IN_COMMAND_LINE = 1;
	const size_t SUCCESS = 0;
	const size_t ERROR_UNHANDLED_EXCEPTION = 2;
}  // namespace


int main(int argc, char** argv)
{
	try
	{
		/* Define and parse programm option
		 */
		namespace po = boost::program_options;
		namespace fs = boost::filesystem;
		po::options_description desc;
		desc.add_options()
			("help,h", "Print help messages")
			("input,i", po::value<std::string>(), "Input directory");

		po::variables_map vm;
        po::store(po::parse_command_line(argc, argv, desc), vm);
        po::notify(vm);  
		try
		{
			po::store(po::parse_command_line(argc, argv, desc),vm);;

			/* --help option
			 */
			if (vm.count("help") )
			{
				std::cout << "Basic Command Line Parameter App" << std::endl << desc << std::endl;
				return SUCCESS;
			}

			po::notify(vm); //throws on error, so do after help in case there are any problems
		}
		catch(po::error& e)
		{
			std::cerr << "ERROR: " << e.what() << std::endl << std::endl;
			std::cerr << desc << std::endl;
			return ERROR_IN_COMMAND_LINE;
		}
        
        // aplication code her //
        
        // output file from directory given
        std::cout << vm["input"].as<std::string>() << std::endl;
        
        fs::path p (vm["input"].as<std::string>());   // p reads input in the following code

        try
        {
          if (fs::exists(p))    // does p actually exist?
          {
            if (fs::is_regular_file(p))        // is p a regular file?   
              std::cout << p << " size is " << fs::file_size(p) << '\n';

            else if (fs::is_directory(p))      // is p a directory?
            {
                typedef std::vector<fs::path> vec;             // store paths,
                vec v;                                // so we can sort them later

                std::copy(fs::directory_iterator(p), fs::directory_iterator(), std::back_inserter(v));

                std::sort(v.begin(), v.end());             // sort, since directory iteration
                                              // is not ordered on some file systems
  
                for (vec::const_iterator it (v.begin()); it != v.end(); ++it)
                {
                    std::cout << "   " << *it << '\n';
                }
            }
            else
              std::cout << p << " exists, but is neither a regular file nor a directory\n";
          }
          else
            std::cout << p << " does not exist\n";
        }
        catch (const fs::filesystem_error& ex)
        {
          std::cout << ex.what() << '\n';
        }
		
	}
	catch(std::exception& e)
	{
		std::cerr << "Unhandled Exception reached the top of main: " << e.what() << ", application will now exit" << std::endl;
		return ERROR_UNHANDLED_EXCEPTION;
	}
	
	
	
	return SUCCESS;
}
