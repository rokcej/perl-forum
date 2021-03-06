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

# Get list of topics
my $topics_list = "";
my @topics = sort { lc($a->{name}) cmp lc($b->{name}) } get_topics();
for my $i (0 .. $#topics) {
	my $id = $topics[$i]{id};
	my $name = $topics[$i]{name};
	my @threads = get_threads($id);

	# Apply search query
	if ($search) {
		my $thread_matches = 0;
		my $hide = 1;

		my $new_name = $name;
		$new_name =~ s/(\Q$query\E)/<span class="text-primary">$1<\/span>/gi;

		# Check thread title for match
		if (!($new_name eq $name)) {
			$name = $new_name;
			$hide = 0;
		}

		# Check replies for matches
		for my $j (0 .. $#threads) {
			if (index(lc($threads[$j]{name}), lc($query)) != -1) {
				$thread_matches++;
			}
		}
		if ($thread_matches > 0) {
			$hide = 0;
			my $thread_matches_string = ($thread_matches == 1 ? "$thread_matches thread" : "$thread_matches threads");
			$name .= " <span class=\"badge badge-primary\">$thread_matches_string</span>";
		}

		if ($hide) {
			next;
		}
	}

	my $num_threads = @threads;
	my $num_threads_string = $num_threads == 1 ? "$num_threads thread" : "$num_threads threads";

	$topics_list .= <<EOS;
<a class="py-4 topic list-group-item list-group-item-action" href=\"threads.cgi?topic_id=$id\">
	<span class="topic-name"><i class="fas fa-angle-right"></i> $name</span>
	<span class="text-black-50 float-right mt-1">$num_threads_string</span>
</a>
EOS
}

# Notice above topic list
my $notice = "";
if ($topics_list eq "") { # If topic list empty
	if ($search && $#topics > -1) {
		$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	No topics match the search query "$query"
</div>
EOS
	} else {
		$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	There are no topics yet
</div>
EOS
	}
} else { # Topic list not empty
	if ($search) {
		$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	Showing search results for "$query"
</div>
EOS
	}
}

print html_header("Topics");
print <<EOS;
<div class="container">
	<nav aria-label="breadcrumb">
		<ol class="my-3 breadcrumb">
			<li class="breadcrumb-item text-truncate active" aria-current="page">Topics</li>
		</ol>
	</nav>

	<form class="my-3" action="topics.cgi" method="get">
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
				<input class="btn btn-primary" type="submit" value="Search " />
			</div>
		</div>
	</form>

<script>
function showCreateTopicForm() {
	document.getElementById("createTopicButton").style.display = "none";
	document.getElementById("createTopicForm").style.display = "inline";
	document.getElementById("createTopicInput").focus(); 
}
</script>

	<div class="mb-4">
		<div class="">
			<h1 class="topics-title mb-3 mr-2">
				Topics
			</h1>
			<div class="d-inline-block align-top my-2">
				<a id="createTopicButton" class="btn btn-primary align-top" href="#" role="button" onclick="showCreateTopicForm();"><i class="fas fa-folder-plus"></i>&nbsp;Create a new topic</a>
				<form id="createTopicForm" class="align-top" action="create_topic.cgi" method="post" style="display: none;">
					<div class="d-inline-flex flex-row">
						<div class="mr-2">
							<input id="createTopicInput" class="form-control" type="text" name="topic_name" size="40" placeholder="Enter new topic name" />
						</div>
						<div class="ml-2">
							<input class="btn btn-primary" type="submit" value="Create topic" />
						</div>
					</div>
				</form>
			</div>
		</div>
		$notice
		<div class="list-group">
			$topics_list
		</div>
	</div>
</div>
EOS
print html_footer();
