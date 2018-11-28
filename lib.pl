use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

sub get_topics { # ()
	my $topics_dir = "topics";
	my $topics_file = "$topics_dir/topics.txt";

	# Create required dirs / files if they don't exist
	if (!(-e $topics_dir && -d $topics_dir)) {
		mkdir($topics_dir);
	}
	if (!(-e $topics_file && -f $topics_file)) {
		open(OUT, ">>", $topics_file) || die "Can't open $topics_file";
		close(OUT);
	}

	# Get topics
	open(IN, "<", $topics_file) || die "Can't open $topics_file";
	my @topics_lines = <IN>;
	close(IN);

	my @topics = ();
	for my $i (0 .. $#topics_lines) {
		chomp($topics_lines[$i]);
		my @data = split(/ /, $topics_lines[$i], 2);
		push(@topics, {
			id => $data[0], 
			name => $data[1]
		});
	}

	return @topics;
}

sub get_threads { # (int topic_id)
	my $topic_id = $_[0];
	my $threads_dir = "topics/$topic_id";
	my $threads_file = "$threads_dir/threads.txt";

	# Create required dirs / files if they don't exist
	if (!(-e $threads_dir && -d $threads_dir)) {
		mkdir($threads_dir);
	}
	if (!(-e $threads_file && -f $threads_file)) {
		open(OUT, ">>", $threads_file) || die "Can't open $threads_file";
		close(OUT);
	}

	# Get threads
	open(IN, "<", $threads_file) || die "Can't open $threads_file";
	my @threads_lines = <IN>;
	close(IN);

	my @threads = ();
	for my $i (0 .. $#threads_lines) {
		chomp($threads_lines[$i]);
		my @data = split(/ /, $threads_lines[$i], 2);
		push(@threads, {
			id => $data[0], 
			name => $data[1]
		});
	}

	return @threads;
}

sub get_replies { # (int topic_id, int thread_id)
	my $topic_id = $_[0];
	my $thread_id = $_[1];
	my $replies_file = "topics/$topic_id/$thread_id.txt";

	# Create required files
	if (!(-e $replies_file && -f $replies_file)) {
		open(OUT, ">>", $replies_file) || die "Can't open $replies_file";
		close(OUT);
	}

	# Get posts
	open(IN, "<", $replies_file) || die "Can't open $replies_file";
	my @replies_lines = <IN>;
	close(IN);

	my @replies = ();
	my $i = 0;
	while ($i <= $#replies_lines) {
		chomp($replies_lines[$i]);
		my @data = split(/ /, $replies_lines[$i], 2);
		$i++;
		chomp($replies_lines[$i]);
		my $text = $replies_lines[$i];
		$i++;

		push(@replies, {
			id => $data[0], 
			name => $data[1],
			text => $text
		});
	}

	return @replies;
}

sub html_header { # (string title)
	return header() . <<EOS;
<html>
<head>
	<title>$_[0]</title>
</head>
<body>
<p><a href="index.cgi">Home</a></p>
EOS
}

sub html_footer { # ()
	return <<EOS;
<p>&copy; 2018 Rok Cej</p>
</body>
</html>
EOS
}

sub html_error { # (string message)
	return html_header("Error") . <<EOS . html_footer();
<h3>Error: $_[0]</h3>
EOS
}

1;
