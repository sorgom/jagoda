use strict;

$\ = "\n";
$, = "\n";

my $rx1 = qr{Node-path: (.*)/.*\RNode-kind: file};
my $rx2 = qr{Node-path: iad/(.*)\RNode-kind: file};
# my $rx = qr/^Node-path\: (.*?)/;
my %map; 

my $path = 'D:/TEMP/svn_dump.txt';

print 'opening ...';




my $fh;
my $content;

open($fh, $path) or die 'open error';

read($fh, $_, -s $path);

print 'size', length($_);

# $map{$1} = 1 
while (m/$rx2/g)
{
    $map{$1} = 1;
}

print length(keys %map);

print sort keys %map;

close($fh);

