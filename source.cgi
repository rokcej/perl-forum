#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

my $file = xss(param("file"));

# Check paramters
if ($file eq "") {
	print html_error("No file selected");
	exit 0;
}

# Make sure file exists and the file is on the list
my @valid_files = get_source_files();
my $valid = 0;
for my $valid_file (@valid_files) {
	if ($file eq $valid_file) {
		$valid = 1;
		last;
	}
}
if (!$valid) {
	print html_error("Invalid file selected");
	exit 0;
}

# Read file
open(IN, "<", $file) || die "Can't read $file";
my @lines = <IN>;
close(IN);

my $code = xss(join("", @lines));

print html_header($file);
print <<EOS;

<div class="container">
	<h1 class="mt-5 mb-4">
		<i class="fas fa-file-code"></i> $file
	</h1>
<pre class="py-3 px-4"><code class="">$code</code></pre>
</div>
EOS
print html_footer();
