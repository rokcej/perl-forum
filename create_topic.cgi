#!C:\Perl64\bin\perl.exe -w

use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

require "./lib.pl";

sub check_topic_params { # (string topic_name)
	# Constants
	my $max_topic_name_length = 100;

	my $topic_name = $_[0];
	## Topic name
	# Check if topic name is valid
	if ($topic_name eq "") {
		return "Topic name can't be empty";
	}
	# Check if topic name is not too long
	if (length($topic_name) > $max_topic_name_length) {
		return "Topic name is too long";
	}
	return "";
}


# Constants
my $max_topics = 10;

# Parameters
my $topic_name = parse_name(xss(param("topic_name")));

# Check for parameter errors
my $err = check_topic_params($topic_name);
if (!($err eq "")) {
	print html_error($err);
	exit 0;
}

# Check if too many topics exist
my @topics = get_topics();
my $num_topics = @topics;
if ($num_topics >= $max_topics) {
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
my $topics_file = "./data/topics/topics.txt";
open(OUT, ">>", $topics_file) || die "Can't open $topics_file";
print OUT "$topic_id $topic_name\n";
close(OUT);

# Redirect user to new topic
print header();
print header();
print <<EOS;
<script type="text/javascript">
	location.replace("threads.cgi?topic_id=$topic_id");
</script>
Topic successfully created. Click <a href="threads.cgi?topic_id=$topic_id">here</a> if you aren't automatically redirected.
EOS
