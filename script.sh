# Run docker mysql container
cd mysql_database
docker build -t {name_image}:{tag_image} .
docker run --name {name_container} -dp {port}:{port_expose} -e MYSQL_ROOT_PASSWORD={passwords} {name_image}:{tag_image}

# Run docker data_crawling container
cd data_crawling
docker build -t {name_image}:{tag_image} .
docker run --name {name_container} -dp {port}:{port_expose} {name_image}:{tag_image}