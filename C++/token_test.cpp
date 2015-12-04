#include <vector>
#include <bitset>
#include <iostream>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/timer.hpp>

using namespace std;
size_t const N = 10000000;

template<typename C>
void test_custom(string const& s, char const* d, C& ret)
{
  C output;

  bitset<255> delims;
  while( *d )
   {
    unsigned char code = *d++;
    delims[code] = true;
  }
  typedef string::const_iterator iter;
  iter beg;
  bool in_token = false;
  for( string::const_iterator it = s.begin(), end = s.end();
    it != end; ++it )
  {
    if( delims[*it] )
    {
      if( in_token )
      {
        output.push_back(typename C::value_type(beg, it));
        in_token = false;
      }
    }
    else if( !in_token )
    {
      beg = it;
      in_token = true;
    }
  }
  if( in_token )
    output.push_back(typename C::value_type(beg, s.end()));
  output.swap(ret);
}

template<typename C>
void test_strpbrk(string const& s, char const* delims, C& ret)
{
  C output;

  char const* p = s.c_str();
  char const* q = strpbrk(p+1, delims);
  for( ; q != NULL; q = strpbrk(p, delims) )
  {
    output.push_back(typename C::value_type(p, q));
    p = q + 1;
  }

  output.swap(ret);
}

template<typename C>
void test_boost(string const& s, char const* delims)
{
  C output;
  boost::split(output, s, boost::is_any_of(delims));
}

int main()
{
  // Generate random text
  string text(N, ' ');
  for( size_t i = 0; i != N; ++i )
    text[i] = (i % 2 == 0)?('a'+(i/2)%26):((i/2)%2?' ':'\t');

  char const* delims = " \t[],-'/\\!\"§$%&=()<>?";

  // Output strings
  boost::timer timer;
  test_boost<vector<string> >(text, delims);
  cout << "Time: " << timer.elapsed() << endl;

  // Output string views
  typedef string::const_iterator iter;
  typedef boost::iterator_range<iter> string_view;
  timer.restart();
  test_boost<vector<string_view> >(text, delims);
  cout << "Time: " << timer.elapsed() << endl;

  // Custom split
  timer.restart();
  vector<string> vs;
  test_custom(text, delims, vs);
  cout << "Time: " << timer.elapsed() << endl;

  // Custom split
  timer.restart();
  vector<string_view> vsv;
  test_custom(text, delims, vsv);
  cout << "Time: " << timer.elapsed() << endl;

  // Custom split
  timer.restart();
  vector<string> vsp;
  test_strpbrk(text, delims, vsp);
  cout << "Time: " << timer.elapsed() << endl;

  // Custom split
  timer.restart();
  vector<string_view> vsvp;
  test_strpbrk(text, delims, vsvp);
  cout << "Time: " << timer.elapsed() << endl;

  return 0;
}
