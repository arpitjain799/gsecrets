import click
from click.testing import CliRunner
import gsecrets

def test_get():
	runner = CliRunner()
	result = runner.invoke(gsecrets.cli.put, [
		"oee-dev-145623/oee-test-secrets/test/foo", 
		"bar"
	])
	assert result.exit_code == 0

	result = runner.invoke(gsecrets.cli.get, [
		"oee-dev-145623/oee-test-secrets/test/foo"
	])
	assert result.exit_code == 0
	assert result.output.strip() == "bar"
