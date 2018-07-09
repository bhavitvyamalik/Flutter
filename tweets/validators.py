from django.core.exceptions import ValidationError

def validate_content(value):
	content=value
	if (content=="stupid") or (content=="shit"):
		raise ValidationError("Stop using cuss words")
	return value
