require('dotenv').config()
const playwright = require('playwright')


const browserType = 'chromium'
const username = process.env.USERNAME
const password = process.env.PASSWORD

async function main() {
    const browser = await playwright[browserType].launch({ headless: false})
    const page = await browser.newPage()

    await page.goto('https://instagram.com/')
    console.log(username)
    console.log(password)
    await browser.close()


}

main()