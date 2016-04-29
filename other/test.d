// Round floating point numbers from stdin

import std.algorithm,
   std.conv,
   std.functional,
   std.math,
   std.regex,
   std.stdio;

// Transforms input into a real number,
// rounds it, then to a string
alias round = pipe!(to!real, std.math.round, to!string);

// Matches numbers that look like they need rounding
static reFloatingPoint = ctRegex!`[0-9]+\.[0-9]+`;

void main(string[] args)
{
   // If arguments, process those and exit,
   // otherwise wait around for input on stdin
   if (args.length > 1)
       args[1..$].map!round.joiner(" ").writeln;
   else
       // Replace anything that looks like a real
       // number with the rounded equivalent.
       stdin.byLine(KeepTerminator.yes)
            .map!(l => l.replaceAll!(c => c.hit.round)
                                    (reFloatingPoint))
            .copy(stdout.lockingTextWriter());
}
