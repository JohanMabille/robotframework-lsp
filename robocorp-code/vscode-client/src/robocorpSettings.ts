// Warning: Don't edit file (autogenerated from python -m dev codegen).

import { WorkspaceConfiguration, workspace } from "vscode";

export function get<T>(key: string): T | undefined {
    var dot = key.lastIndexOf('.');
    var section = key.substring(0, dot);
    var name = key.substring(dot + 1);
    return workspace.getConfiguration(section).get(name);
}

export const ROBOCORP_LANGUAGE_SERVER_TCP_PORT = "robocorp.language-server.tcp-port";
export const ROBOCORP_LANGUAGE_SERVER_ARGS = "robocorp.language-server.args";
export const ROBOCORP_LANGUAGE_SERVER_PYTHON = "robocorp.language-server.python";
export const ROBOCORP_RCC_LOCATION = "robocorp.rcc.location";
export const ROBOCORP_RCC_ENDPOINT = "robocorp.rcc.endpoint";
export const ROBOCORP_RCC_CONFIG_LOCATION = "robocorp.rcc.config_location";

export function getLanguageServerTcpPort(): number {
    let key = ROBOCORP_LANGUAGE_SERVER_TCP_PORT;
    return get<number>(key);
}


export function getLanguageServerArgs(): string[] {
    let key = ROBOCORP_LANGUAGE_SERVER_ARGS;
    return get<string[]>(key);
}


export function getLanguageServerPython(): string {
    let key = ROBOCORP_LANGUAGE_SERVER_PYTHON;
    return get<string>(key);
}


export function getRccLocation(): string {
    let key = ROBOCORP_RCC_LOCATION;
    return get<string>(key);
}


export function getRccEndpoint(): string {
    let key = ROBOCORP_RCC_ENDPOINT;
    return get<string>(key);
}


export function getRccConfigLocation(): string {
    let key = ROBOCORP_RCC_CONFIG_LOCATION;
    return get<string>(key);
}
