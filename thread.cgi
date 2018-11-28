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

# Get topic name
my $topic_name = "";
my @topics = get_topics();
for my $i (0 .. $#topics) {
	if ($topic_id == $topics[$i]{id}) {
		$topic_name = $topics[$i]{name};
		last;
	}
}
if ($topic_name eq "") {
	print html_error("Selected topic doesn't exist");
	exit 0;
}

# Get thread name
my $thread_name = "";
my @threads = get_threads($topic_id);
for my $i (0 .. $#threads) {
	if ($thread_id == $threads[$i]{id}) {
		$thread_name = $threads[$i]{name};
		last;
	}
}
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
