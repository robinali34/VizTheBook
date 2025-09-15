clean:
	@docker-compose kill
	@rm -rf ./data

database:
	@docker run --name cse6242-team-smart-mongo -p 27017:27017 -d mongo:4.4.1
	@mkdir data
	@aws s3 cp s3://cse6242-team-smart-public-data/db.dump ./data/db.dump --no-sign-request
	@docker exec -i $$(docker ps -aqf "name=cse6242-team-smart-mongo") sh -c 'mongorestore -d gutenberg --archive' < ./data/db.dump

install-deps:
	@pip install awscli

run: clean
	@docker-compose up -d --build
	@mkdir data
	@aws s3 cp s3://cse6242-team-smart-public-data/db.dump ./data/db.dump --no-sign-request
	@docker exec -i $$(docker ps -aqf "name=dvasmartteam_db_1") sh -c 'mongorestore -d gutenberg --archive' < ./data/db.dump
