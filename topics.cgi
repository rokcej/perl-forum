#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Get list of topics
my $topics_list = "";
my @topics = get_topics();
for my $i (0 .. $#topics) {
	my $id = $topics[$i]{id};
	my $name = $topics[$i]{name};
	$topics_list .= <<EOS;
<a class="topic-name list-group-item list-group-item-action" href=\"threads.cgi?topic_id=$id\">
	<i class="fas fa-angle-right"></i> $name
</a>
EOS
}
if ($topics_list eq "") {
	$topics_list = <<EOS;
<div class="alert alert-primary alert-trim">
	There are no topics yet.
</div>
EOS
} else {
	$topics_list = <<EOS;
<div class="list-group">
	$topics_list
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

	<form class="my-3" action="create_topic.cgi" method="post">
		<div class="row">
			<div class="col-sm-5">
				<input class="form-control" type="text" name="topic_name" placeholder="Enter new topic name" />
			</div>
			<div class="col-sm">
				<input class="btn btn-primary" type="submit" value="Create Topic" />
			</div>
		</div>
	</form>

	<div class="mb-4">
		<h1 class="my-3">Topics</h1>
		$topics_list
	</div>
</div>
EOS
print html_footer();
