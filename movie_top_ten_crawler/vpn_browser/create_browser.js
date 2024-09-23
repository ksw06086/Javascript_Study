const puppeteer = require('puppeteer');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

function delay(s) {
  return new Promise((resolve) => setTimeout(resolve, s * 1000));
}

function copyProfile(profileName) {
  const profile = path.join(__dirname, 'chrome_profiles', 'profile');
  const newProfile = path.join(__dirname, 'chrome_profiles', profileName);
  fs.cpSync(profile, newProfile, { recursive: true });
  return newProfile;
}

const chromeExecutablePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
// const chromeExecutablePath = "C:\\Users\\jyouk\\AppData\\Local\\Programs\\Opera\\opera.exe";
async function createVpnBrowser(profileName, headless = false) {
  const profilePath = copyProfile(profileName);
  console.log(profilePath);
  const browser = await puppeteer.launch({
    headless: headless ? 'new' : false,
    userDataDir: profilePath,
    ignoreDefaultArgs: ['--disable-extensions', '--enable-automation'],
    args: [
      "--window-size=700,400",
      "--disable-notifications",
      "--window-position=1222,0",
      // '--proxy-server=socks5://127.0.0.1:1080',  // 프록시 설정 (예: SOCKS5 프록시)
      '--disable-blink-features=AutomationControlled',  // 자동화 브라우저 감지 우회
      // '--no-sandbox',
      // '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-infobars',
      '--disable-translate',
      '--disable-extensions',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-web-security',
      '--ignoreHTTPSErrors',
    ],
    executablePath: chromeExecutablePath
  });
  try {
    await delay(3);
    await (await browser.pages())[0].goto('https://ip.pe.kr/');
  }
  catch (e) {
    console.error('Error occurred:', e);
    await browser.close();
    process.exit(1);
  }
  console.log(browser.wsEndpoint());
}

function check_headless(){
  return process.argv[process.argv.length - 1] === 'headless';
}

(async ()=>{
  await createVpnBrowser(uuidv4(), check_headless());
})();