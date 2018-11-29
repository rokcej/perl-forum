#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

print html_header("Forum");
print <<EOS;

<div class="jumbotron jumbotron-fluid my-3 text-center bg-primary">
	<div class="container">
		<h1 class="display-1 text-white">Perl Forum</h1>
		<p class="lead text-light">A simple and anonymous forum open to anyone, anywhere</p>
		<a href="topics.cgi" class="btn btn-light mt-3" role="button"><h1 class="display-4 py-2 px-4">Start Browsing</h1></a>
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
</div>
EOS
print html_footer();
