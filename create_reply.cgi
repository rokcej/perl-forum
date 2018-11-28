#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Constants
my $max_reply_name_length = 100;
my $max_reply_text_length = 1000;
my $max_replies = 100;

# Parameters
my $topic_id = param("topic_id");
my $thread_id = param("thread_id");
my $reply_name = xss(param("reply_name"));
my $reply_text = xss(param("reply_text"));

$reply_name =~ s/\n//g; # Remove newline
$reply_name =~ s/^\s+|\s+$//g; # Remove trailing and leading whitespace
$reply_name =~ s/\s+/ /g; # Remove consequtive whitespace

$reply_text =~ s/\n/<br>/g; # Convert newline to <br>
$reply_text =~ s/^\s+|\s+$//g; # Remove trailing and leading whitespace
$reply_text =~ s/\s+/ /g; # Remove consequtive whitespace
$reply_text =~ s/\s+<br>|<br>\s+/<br>/g; # Get rid of space before or after br
$reply_text =~ s/(<br>){3,}/<br><br>/g; # If more than 2 consequtive <br>, remove the excess

# Check if topic and thread id are valid
if ($topic_id eq "") {
	print html_error("No topic selected");
	exit 0;
}
if ($thread_id eq "") {
	print html_error("No thread selected");
	exit 0;
}

# Check if topic and thread exist
my $topic_name = get_topic_name($topic_id);
if ($topic_name eq "") {
	print html_error("Selected topic doesn't exist");
	exit 0;
}
my $thread_name = get_thread_name($topic_id, $thread_id);
if ($thread_name eq "") {
	print html_error("Selected thread doesn't exist");
	exit 0;
}

# Check if reply name and text are valid
if ($reply_name eq "") {
	print html_error("Your name can't be empty");
	exit 0;
}
if (length($reply_name) > $max_reply_name_length) {
	print html_error("Your name is too long");
	exit 0;
}
if ($reply_text eq "") {
	print html_error("Your message can't be empty");
	exit 0;
}
if (length($reply_text) > $max_reply_text_length) {
	print html_error("Your message is too long");
	exit 0;
}

# Check if too many replies exist
my @replies = get_replies($topic_id, $thread_id);
my $num_replies = @replies;
if ($num_replies > $max_replies) {
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

# Append reply to thread_id.txt
my $replies_file = "topics/$topic_id/$thread_id.txt";
open(OUT, ">>", $replies_file) || die "Can't open $replies_file";
print OUT "$reply_id $reply_name\n";
print OUT "$reply_text\n";
close(OUT);

# Redirect user to new reply
print header();
print <<EOS;
<script type="text/javascript">
	location.replace("thread.cgi?topic_id=$topic_id&thread_id=$thread_id");
</script>
Reply successfully created. Click <a href="thread.cgi?topic_id=$topic_id&thread_id=$thread_id">here</a> if you aren't automatically redirected.
</script>
EOS
