from django.core.exceptions import ValidationError

def validate_content(value):
	content=value
	if (content=="fuck") or (content=="asshole"):
		raise ValidationError("Stop using cuss words")
	return value