build-provisioner:
	@docker build -t aws-ansible:local .

provision-resources:
	@docker run --rm -it \
			-e "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" \
			-e "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" \
			-e "AWS_REGION=${AWS_REGION}" \
			aws-ansible:local /bin/bash provision.sh

decommission-resources:
	@docker run --rm -it \
			-e "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" \
			-e "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" \
			-e "AWS_REGION=${AWS_REGION}" \
			aws-ansible:local /bin/bash decom.sh
