import boto3
import json
import sys, getopt

def verify_region(s3, bucket):
    """
        Verifies if the bucket is in the specified region. 
        Buckets can only be deleted if in the same region as the API call.

        Parameters
        ----------
        s3 : session_token
            the session token authorization for the S3 Client
        bucket : string
            the bucket name passed as an CLI argument
        
        Returns
        -------
        constraint : string || None
            the region where the bucket resides or None if residing in us-east-1
    """
    try:
        response = s3.get_bucket_location(
                Bucket=bucket
            )
    except:
        print("Error getting the bucket location")

    constraint = response['LocationConstraint']

    return constraint

def list_objects(s3, bucket, token=None):
    """
        list objects on Amazon S3. 
        Return a continuation token (pagination) and the response body.

        Parameters
        ----------
        s3 : 
            the session token authorization for the S3 Client
        bucket : 
            the bucket name passed as an CLI argument
        token : string
            the continuation token, if it exists

        Returns
        -------
        response : dict
            the response body of the list_objects_v2 API
        token : string
            a pagination (continuation) token to get the next set of objects
    """
    response = s3.list_objects_v2(
        Bucket=bucket
    )

    if (response['IsTruncated'] != False):
        token = response['NextContinuationToken']
    else:
        token = None
 
    return response, token

def delete_objects(s3, bucket, response, token):
    """
        Delete objects on Amazon S3. 
        If the bucket has more than 1000 objects, loops using the continuation token.

        Parameters
        ----------
        s3 : session_token 
            the session token authorization for the S3 Client
        
        bucket : string
            the bucket name passed as an CLI argument

        response : dict
            the response body provided by list_objects()
        token : string
            the pagination (continuation) token. If it exists will be used for getting more objects.
    """
    objects = []
    
    # if there is a continuation token, we will loop until there is None.
    while (token != None):
        print("More than 1000 objects. Token received: {}".format(token))
        for item in response['Contents']: 
            objects.append( { 'Key': item['Key'] } )

        try:
            s3.delete_objects(
                Bucket=bucket,
                Delete={ 
                    'Objects': objects
                }
            )
        except: 
            print("\tError deleting objects.")
        
        response, token = list_objects(s3, bucket, token)

    # delete the last (or single) batch of objects 
    for item in response['Contents']: 
        objects.append( { 'Key': item['Key'] } )

    try:
        s3.delete_objects(
            Bucket=bucket,
            Delete={ 
                'Objects': objects
            }
        )
    except:
        print("\tError deleting the last \(or single\) batch of objects")

def delete_bucket(s3, bucket):
    """
        Delete the bucket on Amazon S3. Can only be deleted if the bucket is empty.

        Parameters
        ----------
        s3 : session_token 
            the session token authorization for the S3 Client
        bucket : string
            the bucket name passed as an CLI argument
    """
    try:
        s3.delete_bucket(
            Bucket=bucket
        )
    except:
        print("\tError deleting the bucket.")

def main(argv):
    """
        Main logic. 
        Can be used with multiples accounts and principals.
        Creates a specific session using the provided arguments. 
        Verifies if the bucket is in the same region as provided via arguments.
        Empties the bucket before deleting the bucket.

        Parameters
        ----------
        argv : list
            list of arguments received from the command line (CLI)
    """
    try:
        opts, args = getopt.getopt(argv, "b:r:p:", ["bucket=","region=","profile="])
    except getopt.GetoptError:
        print ("delete-buckets.py -b <bucket_name> -r <region> -p <profile>")
        sys.exit(2)

	# TODO: accept a list of buckets instead of just one
    for opt, arg in opts:
        if opt in ("-b", "--bucket"):
            bucket = arg
            print("Bucket set to: ", bucket)
        elif opt in ("-r", "--region"):
            region = arg
            print("Region set to: ", region)
        elif opt in ("-p", "--profile"):
            profile = arg
            print("Profile set to: ", profile)

    # setup boto3 client
    session = boto3.session.Session(profile_name=profile, region_name=region)
    s3 = session.client("s3") 

    constraint = verify_region(s3, bucket)

    if (constraint != None):
        print("bucket not in the same region as requested\n LocationConstraint: {}".format(constraint['LocationConstraint']))
        sys.exit(1)
    else:
        # get a list of all objects and to delete them
        response, token = list_objects(s3, bucket)

        # if there are items, create a list to delete them in a single HTTP call
        if (response['KeyCount'] != 0):
            print("Deleting objects...")
            
            try:
                delete_objects(s3, bucket, response, token)
                print("All objects deleted. Proceding to delete the bucket {} itself.".format(bucket))
            except:
                print("\tError deleting the objects.")

            try:
                delete_bucket(s3, bucket)
                print("Bucket {} deleted.".format(bucket))
            except:
                print("\tError deleting the bucket.")
            
        else:
            print("Bucket {} is already empty".format(bucket))
            
            try:
                delete_bucket(s3, bucket)
                print("Bucket {} deleted.".format(bucket))
            except:
                print("\tError deleting the bucket.")

if __name__ =="__main__":
    main(sys.argv[1:])
