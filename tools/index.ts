import * as Bun from "bun"
import * as Fs from "fs/promises"
import * as Path from "path"

const registry = Path.join(Bun.env.HOME!, "registry")

async function createNewPackage(dependencies: string[]) {
    const name = `pkg_${Date.now().toString(36)}`
    const version = `v${Math.floor(Math.random() * 3)}.${Math.floor(
        Math.random() * 9
    )}.${Math.floor(Math.random() * 9)}`
    await Fs.mkdir(Path.join(registry, name), {recursive: true})
    for (let i = 0; i < Math.random() * 1000; i++) {
        await Bun.write(
            Path.join(registry, name, `file_${i}.gs`),
            `console.log("Hello world ${i} from ${name}!")`
        )
    }
    await Bun.write(
        Path.join(registry, name, "goboscript.toml"),
        `
[dependencies]
${dependencies
    .map((dep) => `${dep.split("@")[0]} = "${registry}/${dep}"`)
    .join("\n")}
`.slice(1)
    )
    await Bun.$`
    cd ${registry}/${name}
    git init
    git add .
    git commit -m "Publish new version: ${version}"
    git tag ${version}`
    return {name, version}
}

const packages: Awaited<ReturnType<typeof createNewPackage>>[] = []

for (let i = 0; i < 1000; i++) {
    const dependencies: string[] = []
    for (let j = 0; j < packages.length / 4; j++) {
        let dep
        while (true) {
            const d = packages[Math.floor(Math.random() * packages.length)]
            dep = `${d.name}@${d.version}`
            if (!dependencies.includes(dep)) {
                break
            }
        }
        dependencies.push(dep)
    }
    packages.push(await createNewPackage(dependencies))
}
