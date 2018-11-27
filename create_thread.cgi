#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Constants
my $max_thread_name_length = 100;
my $max_threads = 100;

# Parameters
my $topic_id = param("topic_id");
my $thread_name = param("thread_name");

$thread_name =~ s/\n//g; # Remove newline,
$thread_name =~ s/^\s+|\s+$//g; # Remove trailing and leading whitespace
$thread_name =~ s/\s{2,}/ /g; # Remove consequtive whitespace

## Topic id
# Check if topic id is valid
if ($topic_id eq "") {
	print html_error("No topic selected");
	exit 0;
}
# Check if topic id exists
my $exists = 0;
my @topics = get_topics();
for my $i (0 .. $#topics) {
	my $id = $topics[$i]{id};
	if ($topic_id == $id) {
		$exists = 1;
		last;
	}
}
if (!$exists) {
	print html_error("Selected topic doesn't exist");
	exit 0;
}

## Thread name
# Check if thread name is valid
if ($thread_name eq "") {
	print html_error("Thread name can't be empty");
	exit 0;
}
# Check if thread name is not too long
if (length($thread_name) > $max_thread_name_length) {
	print html_error("Thread name is too long");
	exit 0;
}

## Create thread
my $thread_id = 0;
my @threads = get_threads($topic_id);
# Check if too many threads exist
my $num_threads = @threads;
if ($num_threads > $max_threads) {
	print html_error("Too many threads already exist");
	exit 0;
}
# Check existing threads
for my $i (0 .. $#threads) {
	my $id = $threads[$i]{id};
	# Increment thread id
	if ($id >= $thread_id) {
		$thread_id = $id + 1;
	}
}
# Append thread to threads.txt
my $threads_file = "topics/$topic_id/threads.txt";
open(OUT, ">>", $threads_file) || die "Can't open $threads_file";
print OUT "$thread_id $thread_name\n";
close(OUT);

# Redirect user to new thread
print header();
print <<EOS;
<script type="text/javascript">
	location.replace("thread.cgi?topic_id=$thread_id&thread_id=$thread_id");
</script>
Thread successfully created. Click <a href="thread.cgi?topic_id=$thread_id&thread_id=$thread_id">here</a> if you aren't automatically redirected.
</script>
EOS
