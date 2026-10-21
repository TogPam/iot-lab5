const { chromium } = require('../tools/browser/node_modules/playwright-core');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');

(async () => {
    const browser = await chromium.launch({
        executablePath: process.env.BROWSER_PATH || 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',
        headless: true,
        args: ['--disable-gpu', '--no-first-run', '--disable-background-networking']
    });
    try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto('http://127.0.0.1:1880/dashboard/gateway');
    await page.getByText('CPU usage', {exact: true}).waitFor();
    await page.getByText('RAM usage', {exact: true}).waitFor();
    await page.getByText('node1', {exact: true}).waitFor({ timeout: 25000 });
    await page.getByText('node2', {exact: true}).waitFor();
    await page.waitForTimeout(5500);
    const body = await page.locator('body').innerText();
    const gaugeValues = await page.locator('.nrdb-ui-gauge-value').allTextContents();
    const chartPresent = await page.locator('.nrdb-ui-chart').count();
    await page.screenshot({ path: path.join(root, 'reports/dashboard.png'), fullPage: true });
    const result = { httpStatus: response.status(), errors, gaugeValues, chartPresent, body };
    fs.writeFileSync(path.join(root, 'reports/dashboard-results.json'), JSON.stringify(result, null, 2));
    await browser.close();
    if (response.status() !== 200 || errors.length || !body.includes('2 nodes') || !chartPresent) {
        throw new Error('Dashboard check failed: see reports/dashboard-results.json');
    }
    console.log('PASS Node-RED Dashboard: CPU/RAM gauges, chart, two live sensor nodes, no browser errors.');
    } finally {
        await browser.close();
    }
})().catch(error => { console.error(error); process.exitCode = 1; });
