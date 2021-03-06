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
	my $time = $replies[$i]{time};
	my $name = $replies[$i]{name};
	my $text = $replies[$i]{text};
	$replies_list .= <<EOS;
<div class="reply border my-2 d-flex flex-row" id="reply$id">
	<div class="p-3 reply-info border-right text-center flex-shrink-0">
		<i class="fas fa-user fa-5x m-1"></i>
		<h4 class="m-1 reply-info-name text-primary">$name</h4>
		<p class="m-1 reply-info-date text-secondary">$time</p>
	</div>
	<div class="p-3 reply-text flex-grow-1">
		<p class="reply">$text</p>
	</div>
</div>
EOS
}

# Notice above reply list
my $notice = "";
if ($replies_list eq "") {
	$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	There aren't any replies to this thread yet
</div>
EOS
}

# Get username from cookie if it exists
my $user_name = cookie("perl-forum-user-name");
my $user_name_input_param = "";
if (!($user_name eq "")) {
	$user_name_input_param = "value=\"$user_name\"";
}

# Print HTML
print html_header($thread_name);
print <<EOS;

<div class="container">
	<nav aria-label="breadcrumb">
		<ol class="my-3 breadcrumb">
			<li class="breadcrumb-item text-truncate"><a href="topics.cgi">Topics</a></li>
			<li class="breadcrumb-item text-truncate"><a href="threads.cgi?topic_id=$topic_id">$topic_name</a></li>
			<li class="breadcrumb-item text-truncate active" aria-current="page">$thread_name</li>
		</ol>
	</nav>

	<div class="mb-4">
		<h1 class="replies-title my-3">$thread_name</h1>
		$notice
		$replies_list
	</div>
</div>
<div class="jumbotron jumbotron-fluid py-4 my-3">
	<div class="container">
		<h2><i class="fas fa-pen"></i>&nbsp;Post a reply</h2>
		<form class="my-3" action="create_reply.cgi" method="post">
			<input type="hidden" name="topic_id" value="$topic_id" />
			<input type="hidden" name="thread_id" value="$thread_id" />
			<div class="input-group my-3">
				<input class="form-control" type="text" name="reply_name" size="40" placeholder="Enter your name" $user_name_input_param />
				<div class="input-group-append">
					<span class="input-group-text">Your name &nbsp; <i class="fas fa-user"></i></span>
				</div>
			</div>
			<div class="input-group my-3">
				<textarea class="form-control" name="reply_text" rows="6" cols="80" placeholder="Enter your message"></textarea>
			</div>
			<div class="input-group my-3">
				<input class="btn btn-primary" type="submit" value="Post reply" />
			</div>
		</form>
	</div>
</div>
EOS
print html_footer();
