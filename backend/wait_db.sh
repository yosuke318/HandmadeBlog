set -e

host="$1"
shift
user="$1"
shift
password="$1"
shift
cmd="$@"

until mysql -h "$mysql_db" -u "$mysql_user" -p"$mysql_password" &> /dev/null
do
  >&2 echo -n "."
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd