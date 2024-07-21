

dev:
	sam build && \
	sam local start-api -l logfile.log


all:
	sam validate && \
	sam build && \
	sam package --region us-east-1 && \
	sam deploy --region us-east-1


