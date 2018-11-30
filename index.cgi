#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

my $views_file = "views.txt";
# Make sure the file exists
if (!(-e $views_file && -f $views_file)) {
	open(OUT, ">>", $views_file) || die "Can't open $views_file";
	close(OUT);
}

# Get views
open(IN, "<", $views_file) || die "Can't open $views_file";
my $num_views = <IN>;
close(IN);
# Increment views
chomp($num_views);
$num_views++;
# Update views
open(OUT, ">", $views_file) || die "Can't open $views_file";
print OUT "$num_views\n";
close(OUT);

my $num_views_string = ($num_views == 1 ? "$num_views time" : "$num_views times");

print html_header("Forum");
print <<EOS;

<div class="jumbotron jumbotron-fluid my-3 text-center bg-primary">
	<div class="container">
		<h1 class="display-1 text-white">Perl Forum</h1>
		<p class="lead text-light">A simple and anonymous forum open to anyone, anywhere</p>
		<a href="topics.cgi" class="btn btn-light mt-3" role="button"><h1 class="display-4 py-2 px-4 breakable-button">Start Browsing</h1></a>
	</div>
</div>

<div class="container">
	<div class="my-5">
		<div class="text-center my-3">
			<h1 class="display-4">Features</h1>
		</div>
		<div class="row">
			<div class="col-sm-4 my-1">
				<div class="card">
					<h5 class="card-header">
						<i class="fas fa-folder"></i> Topics
					</h5>
					<div class="card-body">
						<p class="card-text">You can explore and create different discussion topics, which are sorted alphabetically.</p>
					</div>
				</div>
			</div>
			<div class="col-sm-4 my-1">
				<div class="card">
					<h5 class="card-header">
						<i class="fas fa-file"></i> Threads
					</h5>
					<div class="card-body">
						<p class="card-text">For each topic, you can browse and create new threads, which are sorted by most recent activiy.</p>
					</div>
				</div>
			</div>
			<div class="col-sm-4 my-1">
				<div class="card">
					<h5 class="card-header">
						<i class="fas fa-pen"></i> Replies
					</h5>
					<div class="card-body">
						<p class="card-text">You can read and write your own replies to various threads, which are sorted from newest to oldest.</p>
					</div>
				</div>
			</div>
		</div>
	</div>
	
	<div class="my-5">
		<div class="text-center my-3">
			<h1 class="display-4">Stats</h1>
		</div>
		<div class="text-center my-3">
			<p class="lead ">This homepage has been visited $num_views_string</p>
		</div>
	</div>
</div>
EOS
print html_footer();
