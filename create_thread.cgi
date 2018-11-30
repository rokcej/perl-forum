#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

sub check_thread_params { # (int topic_id, string thread_name, string reply_name, string reply_text)
	# Constants
	my $max_thread_name_length = 100;
	my $max_reply_name_length = 100;
	my $max_reply_text_length = 10000;

	my $topic_id = $_[0];
	my $thread_name = $_[1];
	my $reply_name = $_[2];
	my $reply_text = $_[3];

	# Check if topic id is valid
	if ($topic_id eq "") {
		print html_error("No topic selected");
		exit 0;
	}

	# Check if topic exists
	my $topic_name = get_topic_name($topic_id);
	if ($topic_name eq "") {
		print html_error("Selected topic doesn't exist");
		exit 0;
	}

	# Check if thread name is valid
	if ($thread_name eq "") {
		print html_error("Thread name can't be empty");
		exit 0;
	}
	if (length($thread_name) > $max_thread_name_length) {
		print html_error("Thread name is too long");
		exit 0;
	}

	# Check if reply name and text are valid
	if ($reply_name eq "") {
		return "Your name can't be empty";
	}
	if (length($reply_name) > $max_reply_name_length) {
		return "Your name is too long";
	}
	if ($reply_text eq "") {
		return "Your message can't be empty";
	}
	if (length($reply_text) > $max_reply_text_length) {
		return "Your message is too long";
	}

	return "";
}

# Constants
my $max_threads = 50;

# Parameters
my $topic_id = param("topic_id");
my $thread_name = parse_name(xss(param("thread_name")));
my $reply_name = parse_name(xss(param("reply_name")));
my $reply_text = parse_text(xss(param("reply_text")));

# Check for parameter errors
my $err = check_thread_params($topic_id, $thread_name, $reply_name, $reply_text);
if (!($err eq "")) {
	print html_error($err);
	exit 0;
}

# Check if too many threads exist
my @threads = get_threads($topic_id);
my $num_threads = @threads;
if ($num_threads >= $max_threads) {
	print html_error("Too many threads already exist");
	exit 0;
}

# Get thread id
my $thread_id = 0;
for my $i (0 .. $#threads) {
	my $id = $threads[$i]{id};
	# Increment thread id
	if ($id >= $thread_id) {
		$thread_id = $id + 1;
	}
}

# First reply id will always be 0
my $reply_id = 0;

# Get date time
my @datetime = localtime();
my $date = sprintf("%0004d-%02d-%02d", $datetime[5] + 1900, $datetime[4] + 1, $datetime[3]);
my $time = sprintf("%02d:%02d:%02d", $datetime[2], $datetime[1], $datetime[0]);

# Append thread to threads.txt and reply to thread_id.txt
my $threads_file = "topics/$topic_id/threads.txt";
my $replies_file = "topics/$topic_id/$thread_id.txt";
open(OUT_THREAD, ">>", $threads_file) || die "Can't open $threads_file";
open(OUT_REPLY, ">>", $replies_file) || die "Can't open $replies_file";

print OUT_THREAD "$thread_id $thread_name\n";

print OUT_REPLY "$reply_id $date $time $reply_name\n";
print OUT_REPLY "$reply_text\n";

close(OUT_REPLY);
close(OUT_THREAD);

# Redirect user to new thread
print header();
print <<EOS;
<script type="text/javascript">
	location.replace("replies.cgi?topic_id=$topic_id&thread_id=$thread_id");
</script>
Thread successfully created. Click <a href="replies.cgi?topic_id=$topic_id&thread_id=$thread_id">here</a> if you aren't automatically redirected.
</script>
EOS
