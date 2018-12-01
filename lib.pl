use strict;
use warnings;
use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);

sub xss { # (string text)
	my $text = $_[0];
	$text =~ s/</&lt;/g; # Replace < symbol
	$text =~ s/>/&gt;/g; # Replace > symbol
	return $text;
}

sub parse_name { # (string name)
	my $name = $_[0];

	$name =~ s/\n//g; # Remove newline
	$name =~ s/^\s+|\s+$//g; # Remove trailing and leading whitespace
	$name =~ s/\s+/ /g; # Remove consequtive whitespace

	return $name;
}

sub parse_text { # (string text)
	my $text = $_[0];

	$text =~ s/^\s+|\s+$//g; # Remove trailing and leading whitespace
	$text =~ s/\n/<br>/g; # Convert newline to <br>
	$text =~ s/\s+/ /g; # Remove consequtive whitespace
	$text =~ s/\s+<br>|<br>\s+/<br>/g; # Get rid of space before or after br
	$text =~ s/(<br>){3,}/<br><br>/g; # If more than 2 consequtive <br>, remove the excess

	return $text;
}

sub get_topics { # ()
	my $data_dir = "./data";
	my $topics_dir = "$data_dir/topics";
	my $topics_file = "$topics_dir/topics.txt";

	# Create required dirs / files if they don't exist
	if (!(-e $data_dir && -d $data_dir)) {
		mkdir($data_dir) || die "Can't create $data_dir";
	}
	if (!(-e $topics_dir && -d $topics_dir)) {
		mkdir($topics_dir) || die "Can't create $topics_dir";
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

sub get_topic_name { # (int topic_id)
	my $topic_id = $_[0];

	my @topics = get_topics();
	for my $i (0 .. $#topics) {
		if ($topic_id == $topics[$i]{id}) {
			return $topics[$i]{name};
		}
	}
	return "";
}

sub get_threads { # (int topic_id)
	my $topic_id = $_[0];
	my $threads_dir = "data/topics/$topic_id";
	my $threads_file = "$threads_dir/threads.txt";

	# Create required dirs / files if they don't exist
	if (!(-e $threads_dir && -d $threads_dir)) {
		mkdir($threads_dir) || die "Can't create $threads_dir";
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

sub get_thread_name { # (int topic_id, int thread_id)
	my $topic_id = $_[0];
	my $thread_id = $_[1];

	my @threads = get_threads($topic_id);
	for my $i (0 .. $#threads) {
		if ($thread_id == $threads[$i]{id}) {
			return $threads[$i]{name};
		}
	}
	return "";
}

sub get_replies { # (int topic_id, int thread_id)
	my $topic_id = $_[0];
	my $thread_id = $_[1];
	my $replies_file = "data/topics/$topic_id/$thread_id.txt";

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
		my @data = split(/ /, $replies_lines[$i], 4);
		$i++;
		chomp($replies_lines[$i]);
		my $text = $replies_lines[$i];
		$i++;

		push(@replies, {
			id => $data[0],
			time => "$data[1] $data[2]",
			name => $data[3],
			text => $text
		});
	}

	return @replies;
}

sub html_header { # (string title)
	return header() . <<EOS;
<html>
<head>
    <meta charset="utf-8">
	<title>$_[0]</title>
	<link rel="shortcut icon" href="favicon.ico">
	
<!-- CSS -->
<link rel="stylesheet" href="css/bootstrap.min.css"> <!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous"> <!-- Font Awesome Icons -->
<link rel="stylesheet" href="css/style.css">

</head>
<body>

<nav class="navbar navbar-expand-sm navbar-dark bg-primary">
	<div class="container">
		<a class="navbar-brand" href="index.cgi">Perl Forum</a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav">
			<li class="nav-item">
				<a class="nav-link" href="index.cgi">Home</a>
			</li>
			<li class="nav-item">
				<a class="nav-link" href="topics.cgi">Topics</a>
			</li>
			<li class="nav-item">
				<a class="nav-link" href="about.cgi">About</a>
			</li>
			</ul>
		</div>
	</div>
</nav>

EOS
}

sub html_footer { # ()
	return <<EOS;
<div class="container">
	<hr>
	<footer>
		<p class="footer-text text-center my-3">&copy; 
<script type="text/javascript">
	document.write(new Date().getFullYear());
</script> 
		Rok Cej</p>
	</footer>
</div>

<!-- JS -->
<script src="js/jquery-3.3.1.min.js"></script> <!-- jQuery -->
<script src="js/bootstrap.min.js"></script> <!-- Latest compiled and minified JavaScript -->

</body>
</html>
EOS
}

sub html_error { # (string message)
	return html_header("Error") . <<EOS . html_footer();
<div class="jumbotron my-3">
	<div class="container my-5 text-center">
		<h1 class="display-4"><i class="fas fa-exclamation-triangle fa-3x mb-4"></i></h1>
		<h1 class="display-4">Error: $_[0]</h1>
		<p class="lead">If you believe this is a bug, please contact the administrators</p>
	</div>
</div>
EOS
}

1;
