package AssemblyAPI::AssemblyAPIClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

AssemblyAPI::AssemblyAPIClient

=head1 DESCRIPTION


A KBase module: AssemblyAPI


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => AssemblyAPI::AssemblyAPIClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 search_contigs

  $result = $obj->search_contigs($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is an AssemblyAPI.SearchAssemblyOptions
$result is an AssemblyAPI.SearchAssemblyResult
SearchAssemblyOptions is a reference to a hash where the following keys are defined:
	ref has a value which is a string
	query has a value which is a string
	sort_by has a value which is a reference to a list where each element is an AssemblyAPI.column_sorting
	start has a value which is an int
	limit has a value which is an int
	num_found has a value which is an int
column_sorting is a reference to a list containing 2 items:
	0: (column) a string
	1: (ascending) an AssemblyAPI.boolean
boolean is an int
SearchAssemblyResult is a reference to a hash where the following keys are defined:
	query has a value which is a string
	start has a value which is an int
	contigs has a value which is a reference to a list where each element is an AssemblyAPI.AssemblyData
	num_found has a value which is an int
AssemblyData is a reference to a hash where the following keys are defined:
	contig_id has a value which is a string
	description has a value which is a string
	length has a value which is an int
	gc has a value which is an int
	is_circ has a value which is an int
	N_count has a value which is an int
	md5 has a value which is a string

</pre>

=end html

=begin text

$params is an AssemblyAPI.SearchAssemblyOptions
$result is an AssemblyAPI.SearchAssemblyResult
SearchAssemblyOptions is a reference to a hash where the following keys are defined:
	ref has a value which is a string
	query has a value which is a string
	sort_by has a value which is a reference to a list where each element is an AssemblyAPI.column_sorting
	start has a value which is an int
	limit has a value which is an int
	num_found has a value which is an int
column_sorting is a reference to a list containing 2 items:
	0: (column) a string
	1: (ascending) an AssemblyAPI.boolean
boolean is an int
SearchAssemblyResult is a reference to a hash where the following keys are defined:
	query has a value which is a string
	start has a value which is an int
	contigs has a value which is a reference to a list where each element is an AssemblyAPI.AssemblyData
	num_found has a value which is an int
AssemblyData is a reference to a hash where the following keys are defined:
	contig_id has a value which is a string
	description has a value which is a string
	length has a value which is an int
	gc has a value which is an int
	is_circ has a value which is an int
	N_count has a value which is an int
	md5 has a value which is a string


=end text

=item Description



=back

=cut

 sub search_contigs
{
    my($self, @args) = @_;

# Authentication: optional

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function search_contigs (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to search_contigs:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'search_contigs');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.search_contigs",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'search_contigs',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method search_contigs",
					    status_line => $self->{client}->status_line,
					    method_name => 'search_contigs',
				       );
    }
}
 


=head2 get_assembly_id

  $return = $obj->get_assembly_id($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is a string
ObjectReference is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is a string
ObjectReference is a string


=end text

=item Description

Retrieve Assembly ID.

=back

=cut

 sub get_assembly_id
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_assembly_id (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_assembly_id:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_assembly_id');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_assembly_id",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_assembly_id',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_assembly_id",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_assembly_id',
				       );
    }
}
 


=head2 get_genome_annotations

  $return = $obj->get_genome_annotations($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is a reference to a list where each element is an AssemblyAPI.ObjectReference
ObjectReference is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is a reference to a list where each element is an AssemblyAPI.ObjectReference
ObjectReference is a string


=end text

=item Description

Retrieve associated GenomeAnnotation objects.

@return List of GenomeAnnotation object references

=back

=cut

 sub get_genome_annotations
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_genome_annotations (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_genome_annotations:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_genome_annotations');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_genome_annotations",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_genome_annotations',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_genome_annotations",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_genome_annotations',
				       );
    }
}
 


=head2 get_external_source_info

  $return = $obj->get_external_source_info($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is an AssemblyAPI.AssemblyExternalSourceInfo
ObjectReference is a string
AssemblyExternalSourceInfo is a reference to a hash where the following keys are defined:
	external_source has a value which is a string
	external_source_id has a value which is a string
	external_source_origination_date has a value which is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is an AssemblyAPI.AssemblyExternalSourceInfo
ObjectReference is a string
AssemblyExternalSourceInfo is a reference to a hash where the following keys are defined:
	external_source has a value which is a string
	external_source_id has a value which is a string
	external_source_origination_date has a value which is a string


=end text

=item Description

Retrieve the external source information for this Assembly.

@return Metadata about the external source

=back

=cut

 sub get_external_source_info
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_external_source_info (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_external_source_info:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_external_source_info');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_external_source_info",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_external_source_info',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_external_source_info",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_external_source_info',
				       );
    }
}
 


=head2 get_stats

  $return = $obj->get_stats($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is an AssemblyAPI.AssemblyStats
ObjectReference is a string
AssemblyStats is a reference to a hash where the following keys are defined:
	num_contigs has a value which is an AssemblyAPI.i64
	dna_size has a value which is an AssemblyAPI.i64
	gc_content has a value which is an AssemblyAPI.double
i64 is an int
double is a float

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is an AssemblyAPI.AssemblyStats
ObjectReference is a string
AssemblyStats is a reference to a hash where the following keys are defined:
	num_contigs has a value which is an AssemblyAPI.i64
	dna_size has a value which is an AssemblyAPI.i64
	gc_content has a value which is an AssemblyAPI.double
i64 is an int
double is a float


=end text

=item Description

Retrieve the derived statistical information about this Assembly.

=back

=cut

 sub get_stats
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_stats (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_stats:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_stats');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_stats",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_stats',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_stats",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_stats',
				       );
    }
}
 


=head2 get_number_contigs

  $return = $obj->get_number_contigs($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is an int
ObjectReference is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is an int
ObjectReference is a string


=end text

=item Description

Retrieve the number of contigs for this Assembly.

@return Total number of contiguous sequences.

=back

=cut

 sub get_number_contigs
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_number_contigs (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_number_contigs:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_number_contigs');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_number_contigs",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_number_contigs',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_number_contigs",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_number_contigs',
				       );
    }
}
 


=head2 get_gc_content

  $return = $obj->get_gc_content($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is an AssemblyAPI.double
ObjectReference is a string
double is a float

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is an AssemblyAPI.double
ObjectReference is a string
double is a float


=end text

=item Description

Retrieve the total GC content for this Assembly.

@return Proportion of GC content, between 0 and 1.

=back

=cut

 sub get_gc_content
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_gc_content (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_gc_content:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_gc_content');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_gc_content",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_gc_content',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_gc_content",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_gc_content',
				       );
    }
}
 


=head2 get_dna_size

  $return = $obj->get_dna_size($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is an int
ObjectReference is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is an int
ObjectReference is a string


=end text

=item Description

Retrieve the total DNA size for this Assembly.

@return Total DNA size

=back

=cut

 sub get_dna_size
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_dna_size (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_dna_size:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_dna_size');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_dna_size",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_dna_size',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_dna_size",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_dna_size',
				       );
    }
}
 


=head2 get_contig_ids

  $return = $obj->get_contig_ids($ref)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$return is a reference to a list where each element is a string
ObjectReference is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$return is a reference to a list where each element is a string
ObjectReference is a string


=end text

=item Description

Retrieve the contig identifiers for this Assembly.

@return List of contig IDs.

=back

=cut

 sub get_contig_ids
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_contig_ids (received $n, expecting 1)");
    }
    {
	my($ref) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_contig_ids:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_contig_ids');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_contig_ids",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_contig_ids',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_contig_ids",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_contig_ids',
				       );
    }
}
 


=head2 get_contig_lengths

  $return = $obj->get_contig_lengths($ref, $contig_id_list)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$contig_id_list is a reference to a list where each element is a string
$return is a reference to a hash where the key is a string and the value is an int
ObjectReference is a string

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$contig_id_list is a reference to a list where each element is a string
$return is a reference to a hash where the key is a string and the value is an int
ObjectReference is a string


=end text

=item Description

Retrieve the lengths of the contigs in this Assembly.

@return Mapping of contig ID to contig length.

=back

=cut

 sub get_contig_lengths
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 2)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_contig_lengths (received $n, expecting 2)");
    }
    {
	my($ref, $contig_id_list) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        (ref($contig_id_list) eq 'ARRAY') or push(@_bad_arguments, "Invalid type for argument 2 \"contig_id_list\" (value was \"$contig_id_list\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_contig_lengths:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_contig_lengths');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_contig_lengths",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_contig_lengths',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_contig_lengths",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_contig_lengths',
				       );
    }
}
 


=head2 get_contig_gc_content

  $return = $obj->get_contig_gc_content($ref, $contig_id_list)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$contig_id_list is a reference to a list where each element is a string
$return is a reference to a hash where the key is a string and the value is an AssemblyAPI.double
ObjectReference is a string
double is a float

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$contig_id_list is a reference to a list where each element is a string
$return is a reference to a hash where the key is a string and the value is an AssemblyAPI.double
ObjectReference is a string
double is a float


=end text

=item Description

Retrieve the gc content for contigs in this Assembly.

@return Mapping of contig IDs to GC content proportion.

=back

=cut

 sub get_contig_gc_content
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 2)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_contig_gc_content (received $n, expecting 2)");
    }
    {
	my($ref, $contig_id_list) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        (ref($contig_id_list) eq 'ARRAY') or push(@_bad_arguments, "Invalid type for argument 2 \"contig_id_list\" (value was \"$contig_id_list\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_contig_gc_content:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_contig_gc_content');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_contig_gc_content",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_contig_gc_content',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_contig_gc_content",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_contig_gc_content',
				       );
    }
}
 


=head2 get_contigs

  $return = $obj->get_contigs($ref, $contig_id_list)

=over 4

=item Parameter and return types

=begin html

<pre>
$ref is an AssemblyAPI.ObjectReference
$contig_id_list is a reference to a list where each element is a string
$return is a reference to a hash where the key is a string and the value is an AssemblyAPI.AssemblyContig
ObjectReference is a string
AssemblyContig is a reference to a hash where the following keys are defined:
	contig_id has a value which is a string
	sequence has a value which is a string
	length has a value which is an AssemblyAPI.i64
	gc_content has a value which is an AssemblyAPI.double
	md5 has a value which is a string
	name has a value which is a string
	description has a value which is a string
	is_complete has a value which is an AssemblyAPI.bool
	is_circular has a value which is an AssemblyAPI.bool
i64 is an int
double is a float
bool is an int

</pre>

=end html

=begin text

$ref is an AssemblyAPI.ObjectReference
$contig_id_list is a reference to a list where each element is a string
$return is a reference to a hash where the key is a string and the value is an AssemblyAPI.AssemblyContig
ObjectReference is a string
AssemblyContig is a reference to a hash where the following keys are defined:
	contig_id has a value which is a string
	sequence has a value which is a string
	length has a value which is an AssemblyAPI.i64
	gc_content has a value which is an AssemblyAPI.double
	md5 has a value which is a string
	name has a value which is a string
	description has a value which is a string
	is_complete has a value which is an AssemblyAPI.bool
	is_circular has a value which is an AssemblyAPI.bool
i64 is an int
double is a float
bool is an int


=end text

=item Description

Retrieve all the data for the contigs in this Assembly.

@return Mapping of contig ID to details for that contig.

=back

=cut

 sub get_contigs
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 2)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_contigs (received $n, expecting 2)");
    }
    {
	my($ref, $contig_id_list) = @args;

	my @_bad_arguments;
        (!ref($ref)) or push(@_bad_arguments, "Invalid type for argument 1 \"ref\" (value was \"$ref\")");
        (ref($contig_id_list) eq 'ARRAY') or push(@_bad_arguments, "Invalid type for argument 2 \"contig_id_list\" (value was \"$contig_id_list\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_contigs:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_contigs');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "AssemblyAPI.get_contigs",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_contigs',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_contigs",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_contigs',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "AssemblyAPI.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "AssemblyAPI.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'get_contigs',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method get_contigs",
            status_line => $self->{client}->status_line,
            method_name => 'get_contigs',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for AssemblyAPI::AssemblyAPIClient\n";
    }
    if ($sMajor == 0) {
        warn "AssemblyAPI::AssemblyAPIClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

Indicates true or false values, false = 0, true = 1
@range [0,1]


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 column_sorting

=over 4



=item Definition

=begin html

<pre>
a reference to a list containing 2 items:
0: (column) a string
1: (ascending) an AssemblyAPI.boolean

</pre>

=end html

=begin text

a reference to a list containing 2 items:
0: (column) a string
1: (ascending) an AssemblyAPI.boolean


=end text

=back



=head2 SearchAssemblyOptions

=over 4



=item Description

num_found - optional field which when set informs that there
    is no need to perform full scan in order to count this
    value because it was already done before; please don't
    set this value with 0 or any guessed number if you didn't 
    get right value previously.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ref has a value which is a string
query has a value which is a string
sort_by has a value which is a reference to a list where each element is an AssemblyAPI.column_sorting
start has a value which is an int
limit has a value which is an int
num_found has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ref has a value which is a string
query has a value which is a string
sort_by has a value which is a reference to a list where each element is an AssemblyAPI.column_sorting
start has a value which is an int
limit has a value which is an int
num_found has a value which is an int


=end text

=back



=head2 AssemblyData

=over 4



=item Description

contig_id - id of the contig
description - description of the contig (description on fasta header rows)
length - (bp) length of the contig
gc - gc_content of the contig
is_circ - 0 or 1 value indicating if the contig is circular.  May be null
          if unknown
N_count - number of 'N' bases in the contig
md5 - md5 checksum of the sequence


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
contig_id has a value which is a string
description has a value which is a string
length has a value which is an int
gc has a value which is an int
is_circ has a value which is an int
N_count has a value which is an int
md5 has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
contig_id has a value which is a string
description has a value which is a string
length has a value which is an int
gc has a value which is an int
is_circ has a value which is an int
N_count has a value which is an int
md5 has a value which is a string


=end text

=back



=head2 SearchAssemblyResult

=over 4



=item Description

num_found - number of all items found in query search (with 
    only part of it returned in "bins" list).


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
query has a value which is a string
start has a value which is an int
contigs has a value which is a reference to a list where each element is an AssemblyAPI.AssemblyData
num_found has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
query has a value which is a string
start has a value which is an int
contigs has a value which is a reference to a list where each element is an AssemblyAPI.AssemblyData
num_found has a value which is an int


=end text

=back



=head2 ObjectReference

=over 4



=item Description

Insert your typespec information here.


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 i64

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 double

=over 4



=item Definition

=begin html

<pre>
a float
</pre>

=end html

=begin text

a float

=end text

=back



=head2 bool

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 AssemblyStats

=over 4



=item Description

*
* Derived statistical information about an assembly.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
num_contigs has a value which is an AssemblyAPI.i64
dna_size has a value which is an AssemblyAPI.i64
gc_content has a value which is an AssemblyAPI.double

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
num_contigs has a value which is an AssemblyAPI.i64
dna_size has a value which is an AssemblyAPI.i64
gc_content has a value which is an AssemblyAPI.double


=end text

=back



=head2 AssemblyExternalSourceInfo

=over 4



=item Description

*
* Metadata about the external source of this Assembly.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
external_source has a value which is a string
external_source_id has a value which is a string
external_source_origination_date has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
external_source has a value which is a string
external_source_id has a value which is a string
external_source_origination_date has a value which is a string


=end text

=back



=head2 AssemblyContig

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
contig_id has a value which is a string
sequence has a value which is a string
length has a value which is an AssemblyAPI.i64
gc_content has a value which is an AssemblyAPI.double
md5 has a value which is a string
name has a value which is a string
description has a value which is a string
is_complete has a value which is an AssemblyAPI.bool
is_circular has a value which is an AssemblyAPI.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
contig_id has a value which is a string
sequence has a value which is a string
length has a value which is an AssemblyAPI.i64
gc_content has a value which is an AssemblyAPI.double
md5 has a value which is a string
name has a value which is a string
description has a value which is a string
is_complete has a value which is an AssemblyAPI.bool
is_circular has a value which is an AssemblyAPI.bool


=end text

=back



=cut

package AssemblyAPI::AssemblyAPIClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
