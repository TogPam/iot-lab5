module.exports = {
    uiPort: 1880,
    uiHost: '127.0.0.1',
    flowFile: 'flows.json',
    flowFilePretty: true,
    // Restrict the editor/dashboard to the local computer for this lab.
    diagnostics: { enabled: false },
    runtimeState: { enabled: false },
    logging: { console: { level: 'info', metrics: false, audit: false } },
    editorTheme: { projects: { enabled: false } },
    functionExternalModules: false
};
