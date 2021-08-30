import webbrowser
from tkinter import *
from multiprocessing import Pool, cpu_count, freeze_support
from selenium import webdriver
from fake_useragent import UserAgent
import random

count = 0


def get_proxies(ua):
    proxies = []
    # file1 = open("https://mirindaweb.com/proxy/proxy.txt","r+")
    file1 = open("proxy.txt", "r+")
    Lines = file1.readlines()

    for row in Lines:
        check = row.split(':')
        proxies.append({
            'ip': check[0],
            'port': check[1]
        })
    return proxies


def random_proxy(proxies):
    return random.choice(proxies)


def search_string_to_query(search_string):
    search = search_string.split(' ')
    query = '+'.join(search)
    print("6666666666666666666666666", query)
    return query


def search_and_click(ua, sleep_time, search_string, proxy, proxies, sleep_after, url):
    global count
    print("44444444444444444444444444444444444444444444444444444", count)
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % (proxy['ip'] + ':' + proxy['port']))
    print("cehkasdkasdjsad", proxy['ip'] + ':' + proxy['port'])
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/")

    try:
        section_list = driver.find_element_by_class_name('section-list')

        link = section_list.find_element_by_class_name('yt-uix-tile-link')

        link.click()

        driver.quit()

        if sleep_after is not None:
            sleep(sleep_after)

    except:

        count = count + 1
        print(count)
        proxy = random.choice(proxies)
        search_and_click(ua, sleep_time, search_string, proxy, proxies, sleep_after, url)


def parse_line(line):
    delim_loc = line.find('=')
    return line[delim_loc + 1:].strip()


def read_config(config_string):
    try:
        search_string = parse_line(config_string[0])
        min_watch = int(parse_line(config_string[1]))
        max_watch = int(parse_line(config_string[2]))
        sleep_after = int(parse_line(config_string[3]))
        views = int(parse_line(config_string[4]))
        multicore = parse_line(config_string[5])
        if multicore != 'True':
            multicore = False
        if sleep_after == 'None':
            sleep_after = None
        return search_string, sleep_after, min_watch, max_watch, views, multicore
    except:
        write_defaults()
        return 'Bad File', 'RIP', 'Bad File', 'RIP', 'Bad File', 'RIP'


def write_defaults():
    with open('config.txt', 'w') as config:
        config.write('search_string = Bashar Momin Episode 1\n')
        config.write('min_watch = 10\n')
        config.write('max_watch = 30\n')
        config.write('wait_after = 15\n')
        config.write('views = 5\n')
        config.write('multicore = False')


write_defaults()


def trigger():
    print('000001')
    freeze_support()
    with open('config.txt', 'r') as config:
        config_values = config.readlines()

    url = "https://www.google.com/search?q=whats+my+ip&oq=whats+my+&aqs=chrome.0.35i39j69i57j0i10j0j0i10l2j0j0i10l2j46i10.11995j0j7&sourceid=chrome&ie=UTF-8"

    print('000002')

    search_string, sleep_after, min_watch, max_watch, views, multicore = read_config(config_values)
    if min_watch == 'Bad File':
        i = 'rip'
        print('000003')
    elif multicore:
        print('000004')
        threads = int(cpu_count() * 0.75)
        pool = Pool(threads)
        ua = UserAgent()
        proxies = get_proxies(ua)
        for i in range(views):
            sleep_time = random.randint(min_watch, max_watch)
            proxy = random_proxy(proxies)
            pool.apply_async(search_and_click, args=[ua, sleep_time, search_string, proxy, proxies, sleep_after, url])
        pool.close()
        pool.join()
    else:
        ua = UserAgent()
        proxies = get_proxies(ua)
        for i in range(views):
            sleep_time = random.randint(min_watch, max_watch)
            proxy = random_proxy(proxies)
            search_and_click(ua, 30, search_string, proxy, proxies, 30, url)


root = Tk()
root.geometry("300x300")
label = Label(text="some text")
label.pack()
labelOne = Label(text="A little bit more text")
labelOne.pack()

click = Button(text="Clica Aqui!", command=trigger)
click.pack()
root.mainloop()
