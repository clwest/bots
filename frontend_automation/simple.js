const playwright = require('playwright')

const browserType = 'chromium'

async function main() {
    const browser = await playwright[browserType].launch({ headless: false})
    const context = await browser.newContext()
    const page = await context.newPage()

    await page.goto('https://www.google.com')

    const searchTerm = 'I love automation'
    const input = await page.$('[name="q"]')
    await input.type(searchTerm)
    await input.press('Enter')

    await page.screenshot({path: 'result.png'})
    await browser.close()

}

main()