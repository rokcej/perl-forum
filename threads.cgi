#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Parameters
my $topic_id = param("topic_id");
my $query = parse_name(xss(param("query")));

my $search = ($query eq "" ? 0 : 1);

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

# Get list of threads
my $threads_list = "";
my @threads_unsorted = get_threads($topic_id);
# Sort threads by activity and apply search query
for my $i (0 .. $#threads_unsorted) {
	my $id = $threads_unsorted[$i]{id};
	my @replies = get_replies($topic_id, $id);

	$threads_unsorted[$i]{last_activity} = ($#replies >= 0 ? $replies[$#replies]{time} : "0000-01-01 00:00:00");

	if ($search) {
		my $reply_matches = 0;
		$threads_unsorted[$i]{hide} = 1;

		my $new_name = $threads_unsorted[$i]->{name};
		$new_name =~ s/(\Q$query\E)/<span class="text-primary">$1<\/span>/gi;

		# Check thread title for match
		if (!($new_name eq $threads_unsorted[$i]{name})) {
			$threads_unsorted[$i]{name} = $new_name;
			$threads_unsorted[$i]{hide} = 0;
		}

		# Check replies for matches
		for my $j (0 .. $#replies) {
			if (index(lc($replies[$j]{text}), lc($query)) != -1) {
				$reply_matches++;
			}
		}
		if ($reply_matches > 0) {
			$threads_unsorted[$i]{hide} = 0;
			my $reply_matches_string = ($reply_matches == 1 ? "$reply_matches reply" : "$reply_matches replies");
			$threads_unsorted[$i]{name} .= " <span class=\"badge badge-primary\">$reply_matches_string</span>";
		}
	}

	if (!$search || !$threads_unsorted[$i]{hide}) {
		my $num_replies = @replies;
		$threads_unsorted[$i]{num_replies} = $num_replies;
	}
}
my @threads = sort { $b->{last_activity} cmp $a->{last_activity} } @threads_unsorted;
# Append threads to list
for my $i (0 .. $#threads) {
	if ($search) {
		if ($threads[$i]{hide}) {
			next;
		}
	}

	my $id = $threads[$i]{id};
	my $name = $threads[$i]{name};
	my $last_activity = $threads[$i]{last_activity};
	my $num_replies = $threads[$i]{num_replies};
	my $num_replies_string = $num_replies == 1 ? "$num_replies reply" : "$num_replies replies";

	$threads_list .= <<EOS;
<a class="thread list-group-item list-group-item-action" href=\"replies.cgi?topic_id=$topic_id&thread_id=$id\">
	<span class="thread-name"><i class="fas fa-angle-double-right"></i> $name</span>
	<span class="text-black-50 float-right mt-1">$num_replies_string <i class="fas fa-arrow-right"></i> Last reply $last_activity</span>
</a>
EOS
}

# Notice above thread list
my $notice = "";
if ($threads_list eq "") { # Thread list empty
	if ($search && $#threads > -1) {
		$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	No threads in this topic match the search query "$query"
</div>
EOS
	} else {
		$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	There aren't any threads in this topic yet
</div>
EOS
	}
} else { # Thread list not empty
	if ($search) {
		$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	Showing search results for "$query"
</div>
EOS
	}
}

# Get username from cookie if it exists
my $user_name = cookie("perl-forum-user-name");
my $user_name_input_param = "";
if (!($user_name eq "")) {
	$user_name_input_param = "value=\"$user_name\"";
}

# Print HTML
print html_header($topic_name);
print <<EOS;
<div class="container">
	<nav aria-label="breadcrumb">
		<ol class="my-3 breadcrumb">
			<li class="breadcrumb-item text-truncate"><a href="topics.cgi">Topics</a></li>
			<li class="breadcrumb-item text-truncate active" aria-current="page">$topic_name</li>
		</ol>
	</nav>

	<form class="my-3" action="threads.cgi" method="get">
		<input type="hidden" name="topic_id" value="$topic_id" />
		<div class="d-flex flex-row">
			<div class="mr-2">
				<div class="input-group">
					<input class="form-control" type="text" name="query" size="40" placeholder="Enter search query" />
					<div class="input-group-append">
						<span class="input-group-text" id="basic-addon2"><i class="fas fa-search"></i></span>
					</div>
				</div>
			</div>
			<div class="ml-2">
				<input class="btn btn-primary" type="submit" value="Search" />
			</div>
		</div>
	</form>
	
	<div class="mb-4">
		<h1 class="threads-title my-3">$topic_name</h1>
		$notice
		<div class="list-group">
			$threads_list
		</div>
	</div>
</div>

<div class="jumbotron jumbotron-fluid py-4 my-3">
	<div class="container">
		<h2><i class="fas fa-file"></i>&nbsp;Create a new thread</h2>
		<form class="my-3" action="create_thread.cgi" method="post">
			<input type="hidden" name="topic_id" value="$topic_id" />
			<div class="input-group my-3">
				<input class="form-control" type="text" name="thread_name" size="40" placeholder="Enter thread title" />
				<div class="input-group-append">
					<span class="input-group-text">Thread title &nbsp; <i class="fas fa-tag"></i></span>
				</div>
			</div>
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
				<input class="btn btn-primary" type="submit" value="Create thread" />
			</div>
		</form>
	</div>
</div>
EOS
print html_footer();
