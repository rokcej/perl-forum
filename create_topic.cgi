#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

# Constants
my $max_topic_name_length = 100;
my $max_topics = 20;

# Parameters
my $topic_name = xss(param("topic_name"));

$topic_name =~ s/\n//g; # Remove newline
$topic_name =~ s/^\s+|\s+$//g; # Remove trailing and leading whitespace
$topic_name =~ s/\s+/ /g; # Remove consequtive whitespace


## Topic name
# Check if topic name is valid
if ($topic_name eq "") {
	print html_error("Topic name can't be empty");
	exit 0;
}
# Check if topic name is not too long
if (length($topic_name) > $max_topic_name_length) {
	print html_error("Topic name is too long");
	exit 0;
}

# Check if too many topics exist
my @topics = get_topics();
my $num_topics = @topics;
if ($num_topics > $max_topics) {
	print html_error("Too many topics already exist");
	exit 0;
}

# Check existing topics
my $topic_id = 0;
for my $i (0 .. $#topics) {
	my $id = $topics[$i]{id};
	my $name = $topics[$i]{name};
	# Check if topic name already exists
	if (lc($topic_name) eq lc($name)) {
		print html_error("Topic name already exists");
		exit 0;
	}
	# Increment topic id
	if ($id >= $topic_id) {
		$topic_id = $id + 1;
	}
}

# Append topic to topics.txt
my $topics_file = "topics/topics.txt";
open(OUT, ">>", $topics_file) || die "Can't open $topics_file";
print OUT "$topic_id $topic_name\n";
close(OUT);

# Redirect user to new topic
print header();
print header();
print <<EOS;
<script type="text/javascript">
	location.replace("topic.cgi?topic_id=$topic_id");
</script>
Topic successfully created. Click <a href="topic.cgi?topic_id=$topic_id">here</a> if you aren't automatically redirected.
EOS
