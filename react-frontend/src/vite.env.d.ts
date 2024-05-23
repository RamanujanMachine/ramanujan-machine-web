/// <reference types="vite/client" />

interface ImportMetaEnv {
	readonly VITE_PUBLIC_IP: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
