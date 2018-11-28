#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Parameters
my $topic_id = param("topic_id");
my $thread_id = param("thread_id");

# Check if topic and thread ids are valid
if ($topic_id eq "") {
	print html_error("No topic selected");
	exit 0;
}
if ($thread_id eq "") {
	print html_error("No thread selected");
	exit 0;
}

# Check if topic exists
my $topic_name = get_topic_name($topic_id);
if ($topic_name eq "") {
	print html_error("Selected topic doesn't exist");
	exit 0;
}

# Check if thread exists
my $thread_name = get_thread_name($topic_id, $thread_id);
if ($thread_name eq "") {
	print html_error("Selected thread doesn't exist");
	exit 0;
}

# Get list of replies
my $replies_list = "";
my @replies = get_replies($topic_id, $thread_id);
for my $i (0 .. $#replies) {
	my $id = $replies[$i]{id};
	my $name = $replies[$i]{name};
	my $text = $replies[$i]{text};
	$replies_list .= <<EOS;
<li>
	<p>Posted by: $name</p>
	<p>$text</p>
</li>\n
EOS
}
if ($replies_list eq "") {
	$replies_list = "There aren't any replies to this thread yet"
}

# Print HTML
print html_header($thread_name);
print <<EOS;
<h3><a href="index.cgi">Home</a> > <a href="topic.cgi?topic_id=$topic_id">$topic_name</a> > $thread_name</h3>
<ul>$replies_list</ul>
<form action="create_reply.cgi" method="post">
	<input type="hidden" name="topic_id" value="$topic_id" />
	<input type="hidden" name="thread_id" value="$thread_id" />
	<input type="text" name="reply_name" size="20" placeholder="Enter your name" /> <br>
	<textarea name="reply_text" rows="6" cols="60" placeholder="Enter your message"></textarea> <br>
	<input type="submit" value="Post Reply" />
</form>
EOS
print html_footer();
