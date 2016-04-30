def parse_app_page(response):
    # Should always be able to grab a title
    title = response.xpath('//div[@class = "panel panel-default panel-gameinfo"]/div[@class = "panel-heading"]/text()').extract()[0].strip()
    # Parse times into floats
    time_to_hundo = response.xpath('//table[@class = "Default1000"]/tr/td[span = "Hours to 100%"]/text()[last()]').extract()[0].strip()
    time_to_hundo = time_to_hundo.replace(',', '.')
    time_to_hundo = float(time_to_hundo)
    # Points may or may not be present, default to 0 if absent
    points = response.xpath('//table[@class = "Default1000"]/tr/td[span = "Points"]/text()[last()]').extract()
    if not points:
        points = 0
    else:
        points = int(points[0].strip())

    yield {
        'title': title,
        'time to 100%': time_to_hundo,
        'points': points,
        }


def parse_search_result_for_apps(response):
    for href in response.xpath('//table//table//a/@href'):
        relative_url = href.extract()
        if relative_url.startswith('Steam_Game_Info.php?AppID='):
            yield {
                'app_id' : relative_url[len('Steam_Game_Info.php?AppID='):]
            }
