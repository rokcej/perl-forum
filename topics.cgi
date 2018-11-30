#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Parameters
my $topic_id = param("topic_id");
my $query = xss(param("query"));

my $search = ($query eq "" ? 0 : 1);

# Get list of topics
my $topics_list = "";
my @topics = sort { $a->{name} cmp $b->{name} } get_topics();
for my $i (0 .. $#topics) {
	# Apply search query
	if ($search) {
		
	}


	my $id = $topics[$i]{id};
	my $name = $topics[$i]{name};

	my $num_threads = get_threads($id);
	my $num_threads_string = $num_threads == 1 ? "$num_threads thread" : "$num_threads threads";

	$topics_list .= <<EOS;
<a class="topic list-group-item list-group-item-action" href=\"threads.cgi?topic_id=$id\">
	<span class="topic-name"><i class="fas fa-angle-right"></i> $name</span>
	<span class="text-black-50 float-right mt-1">$num_threads_string</span>
</a>
EOS
}

# Notice above topic list
my $notice = "";
if ($topics_list eq "") { # If topic list empty
	$notice = <<EOS;
<div class="alert alert-primary alert-trim">
	There are no topics yet.
</div>
EOS
}

print html_header("Forum");
print <<EOS;
<div class="container">
	<nav aria-label="breadcrumb">
		<ol class="my-3 breadcrumb">
			<li class="breadcrumb-item active" aria-current="page">Topics</li>
		</ol>
	</nav>

	<form class="my-3" action="topics.cgi" method="get">
		<div class="d-flex flex-row">
			<div class="mr-2">
				<input class="form-control" type="text" name="query" size="40" placeholder="Enter search query" />
			</div>
			<div class="ml-2">
				<input class="btn btn-primary" type="submit" value="Search" />
			</div>
		</div>
	</form>

<script>
function showCreateTopicForm() {
	document.getElementById("createTopicButton").style.display = "none";
	document.getElementById("createTopicForm").style.display = "inline-block";
}
</script>

	<div class="mb-4">
		<div class="d-flex flex-row">
			<h1 class="mb-3">
				Topics
			</h1>
			<div class="mt-2 ml-3">
				<a id="createTopicButton" class="btn btn-primary align-top" href="#" role="button" onclick="showCreateTopicForm();">Create new</a>
				<form id="createTopicForm" action="create_topic.cgi" method="post" style="display: none;">
					<div class="d-flex flex-row">
						<div class="mr-2">
							<input class="form-control" type="text" name="topic_name" size="40" placeholder="Enter new topic name" />
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
