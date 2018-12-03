#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

print html_header("About");
print <<EOS;

<div class="container">
	<div class="my-5">
		<h1 class="">About me</h1>
		<p>
			Thanks for checking out my website!
		</p>
		<p class="">
			My name is Rok and I'm a currently studying computer science at Kyungpook National University in South Korea.
			I made this forum as project for my Web Programming course.
			You can check out my other projects on my <a href="https://github.com/rokcej">Github <i class="fab fa-github"></i></a>.
		</p>
	</div>
	<div class="my-5">
		<h1>About the website</h1>
		<p>
			This website was developed using the CGI module in the <a href="https://www.perl.org/">Perl programming language</a>.
			CGI allows you to execute server-side scripts, providing users with dynamic web content.
			The user interface was designed using <a href="https://getbootstrap.com/">Bootstrap</a>, a CSS framework.
			All the icons were provided by <a href="https://fontawesome.com/">Fontawesome <i class="fab fa-font-awesome-flag"></i></a>.
		</p>
	</div>
	<div class="my-5">
		<h1>Feedback</h1>
		<p>
			If you have any suggestions, ideas for improvement, complaints or if you found any bugs, 
			make sure to let me know by posting a new thread on the forum.
		</p>
	</div>
</div>
EOS
print html_footer();
