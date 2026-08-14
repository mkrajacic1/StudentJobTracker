from student_job_tracker.services.api_scraper import text_from_html


def test_html_parser_from_description():
    html = "<p>poželjna vozačka dozvola B kategorija,&nbsp;student završne godine tehničkog smjera (IT, računarstvo, elektrotehnika) &nbsp;</p>"
    cleaned = "poželjna vozačka dozvola B kategorija, student završne godine tehničkog smjera (IT, računarstvo, elektrotehnika)"
    assert text_from_html(html) == cleaned


def test_html_parser_from_contact():
    html = '<p>&nbsp;poslati molbu i životopis na <a href="mailto:abc@abc.com" rel="noopener noreferrer" target="_blank">abc@abc.com</a></p>'
    cleaned = "poslati molbu i životopis na abc@abc.com"
    assert text_from_html(html) == cleaned


