#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

sub check_reply_params { # (int topic_id, int thread_id, string reply_name, string reply_text)
	# Constants
	my $max_reply_name_length = 100;
	my $max_reply_text_length = 10000;

	my $topic_id = $_[0];
	my $thread_id = $_[1];
	my $reply_name = $_[2];
	my $reply_text = $_[3];

	# Check if topic and thread id are valid
	if ($topic_id eq "") {
		return "No topic selected";
	}
	if ($thread_id eq "") {
		return "No thread selected";
	}

	# Check if topic and thread exist
	my $topic_name = get_topic_name($topic_id);
	if ($topic_name eq "") {
		return "Selected topic doesn't exist";
	}
	my $thread_name = get_thread_name($topic_id, $thread_id);
	if ($thread_name eq "") {
		return "Selected thread doesn't exist";
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
my $max_replies = 200;

# Parameters
my $topic_id = param("topic_id");
my $thread_id = param("thread_id");
my $reply_name = parse_name(xss(param("reply_name")));
my $reply_text = parse_text(xss(param("reply_text")));

# Check for parameter errors
my $err = check_reply_params($topic_id, $thread_id, $reply_name, $reply_text);
if (!($err eq "")) {
	print html_error($err);
	exit 0;
}

# Check if too many replies exist
my @replies = get_replies($topic_id, $thread_id);
my $num_replies = @replies;
if ($num_replies >= $max_replies) {
	print html_error("Too many replies already exist");
	exit 0;
}

# Check existing replies
my $reply_id = 0;
for my $i (0 .. $#replies) {
	my $id = $replies[$i]{id};
	# Increment thread id
	if ($id >= $reply_id) {
		$reply_id = $id + 1;
	}
}

# Get date time
my @datetime = localtime();
my $date = sprintf("%0004d-%02d-%02d", $datetime[5] + 1900, $datetime[4] + 1, $datetime[3]);
my $time = sprintf("%02d:%02d:%02d", $datetime[2], $datetime[1], $datetime[0]);

# Append reply to thread_id.txt
my $replies_file = "./data/topics/$topic_id/$thread_id.txt";
open(OUT, ">>", $replies_file) || die "Can't open $replies_file";
print OUT "$reply_id $date $time $reply_name\n";
print OUT "$reply_text\n";
close(OUT);

# Redirect user to new reply
print header();
print <<EOS;
<script type="text/javascript">
	location.replace("replies.cgi?topic_id=$topic_id&thread_id=$thread_id#reply$reply_id");
</script>
Reply successfully created. Click <a href="replies.cgi?topic_id=$topic_id&thread_id=$thread_id#reply$reply_id">here</a> if you aren't automatically redirected.
</script>
EOS
