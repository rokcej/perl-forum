#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Parameters
my $topic_id = param("topic_id");

# Check if topic id is valid
if ($topic_id eq "") {
	print html_error("No topic selected");
	exit 0;
}

# Get topic name
my $topic_name = "";
my @topics = get_topics();
for my $i (0 .. $#topics) {
	if ($topic_id == $topics[$i]{id}) {
		$topic_name = $topics[$i]{name};
		last;
	}
}

# Check if topic exists
if ($topic_name eq "") {
	print html_error("Selected topic doesn't exist");
	exit 0;
}

# Get list of threads
my $threads_list = "";
my @threads = get_threads($topic_id);
for my $i (0 .. $#threads) {
	my $id = $threads[$i]{id};
	my $name = $threads[$i]{name};
	$threads_list .= "<li><a href=\"thread.cgi?topic_id=$topic_id&thread_id=$id\">$name</a></li>\n";
}

# Print HTML
print html_header($topic_name);
print <<EOS;
<form action="create_thread.cgi" method="post">
	<input type="hidden" name="topic_id" value="$topic_id" />
	<input type="text" name="thread_name" size="40" placeholder="Enter new thread name" />
	<input type="submit" value="Create Thread" />
</form>
<h3><a href="index.cgi">Home</a> > $topic_name</h3>
<ul>$threads_list</ul>
EOS
print html_footer();
