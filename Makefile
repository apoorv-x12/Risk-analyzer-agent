.PHONY: venv install pdf run clean

# # Create a Python virtual environment
# venv:
# 	python -m venv venv

# # Install requirements (edit requirements.txt as needed)
# install:
# 	venv/Scripts/pip install -r requirements.txt

# # Generate sample_contract.pdf from sample_contract.txt using pandoc
# pdf:
# 	pandoc sample_contract.txt -o sample_contract.pdf

# Run the archivist pipeline
run:
	venv/Scripts/python -m agent_archivist.archivist

# # Clean up generated files
# clean:
# 	rm -f sample_contract.pdf
# 	rm -rf venv 