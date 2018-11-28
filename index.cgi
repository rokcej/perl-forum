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
	$topics_list .= "<li><a href=\"topic.cgi?topic_id=$id\">$name</a></li>\n";
}

print html_header("Forum");
print <<EOS;
<form action="create_topic.cgi" method="post">
	<input type="text" name="topic_name" size="40" placeholder="Enter new topic name" />
	<input type="submit" value="Create Topic" />
</form>
<h3>Home</h3>
<ul>$topics_list</ul>
EOS
print html_footer();
