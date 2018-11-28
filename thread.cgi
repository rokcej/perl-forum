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
<div class="card my-1 flex-row">
	<div class="card-body col-2 border-right">
		<h3 class="card-title">$name</h3>
	</div>
	<div class="card-body col-10">
		<p class="card-text">$text</p>
	</div>
</div>
EOS
}
if ($replies_list eq "") {
	$replies_list = <<EOS;
<div class="alert alert-primary alert-trim">
	There aren't any replies to this thread yet.
</div>
EOS
}

# Print HTML
print html_header($thread_name);
print <<EOS;

<div class="container">
	<nav aria-label="breadcrumb">
		<ol class="my-3 breadcrumb">
			<li class="breadcrumb-item"><a href="index.cgi">Topics</a></li>
			<li class="breadcrumb-item"><a href="topic.cgi?topic_id=$topic_id">$topic_name</a></li>
			<li class="breadcrumb-item active" aria-current="page">$thread_name</li>
		</ol>
	</nav>

	<h1>$thread_name</h1>
	$replies_list
</div>
<div class="jumbotron jumbotron-fluid py-4 my-3">
	<div class="container">
		<h2>Post a Reply</h2>
		<form class="my-3" action="create_reply.cgi" method="post">
			<input type="hidden" name="topic_id" value="$topic_id" />
			<input type="hidden" name="thread_id" value="$thread_id" />
			<div class="form-group">
				<input class="form-control" type="text" name="reply_name" size="20" placeholder="Enter your name" />
			</div>
			<div class="form-group">
				<textarea class="form-control" name="reply_text" rows="6" cols="60" placeholder="Enter your message"></textarea>
			</div>
			<div class="form-group">
				<input class="btn btn-primary" type="submit" value="Post Reply" />
			</div>
		</form>
	</div>
</div>
EOS
print html_footer();
