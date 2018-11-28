#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Parameters
my $topic_id = param("topic_id");

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
my @threads = get_threads($topic_id);
for my $i (0 .. $#threads) {
	my $id = $threads[$i]{id};
	my $name = $threads[$i]{name};
	$threads_list .= <<EOS;
<li class=\"list-group-item\">
	<a href=\"thread.cgi?topic_id=$topic_id&thread_id=$id\">$name</a>
</li>
EOS
}
if ($threads_list eq "") {
	$threads_list = <<EOS;
<div class="alert alert-primary alert-trim">
	There aren't any replies to this topic yet.
</div>
EOS
} else {
	$threads_list = <<EOS;
<ul class="list-group">
	$threads_list
</ul>
EOS
}

# Print HTML
print html_header($topic_name);
print <<EOS;
<div class="container">
	<nav aria-label="breadcrumb">
		<ol class="my-3 breadcrumb">
			<li class="breadcrumb-item"><a href="index.cgi">Topics</a></li>
			<li class="breadcrumb-item active" aria-current="page">$topic_name</li>
		</ol>
	</nav>

	<form class="my-3" action="create_thread.cgi" method="post">
			<input type="hidden" name="topic_id" value="$topic_id" />
		<div class="row">
			<div class="col-sm-5">
				<input class="form-control" type="text" name="thread_name" size="40" placeholder="Enter new thread name" />
			</div>
			<div class="col-sm">
				<input class="btn btn-primary" type="submit" value="Create Thread" />
			</div>
		</div>
	</form>

	<h1>$topic_name</h1>
	$threads_list
</div>
EOS
print html_footer();
