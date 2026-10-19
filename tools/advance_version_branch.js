// 时间: 2026-10
// 合并后的版本分支递增小版本号，保留历史及合并后新提交。
"use strict";

function nextVersion(name) {
  const match = /^V(0|[1-9]\d*)\.(0|[1-9]\d*)$/.exec(name || "");
  return match ? `V${match[1]}.${BigInt(match[2]) + 1n}` : null;
}

async function advanceVersionBranch({ github, context, core, wait = ms => new Promise(resolve => setTimeout(resolve, ms)) }) {
  const pr = context.payload.pull_request;
  const fullName = `${context.repo.owner}/${context.repo.repo}`;
  const oldName = pr?.head?.ref;
  const newName = nextVersion(oldName);
  if (!pr?.merged || pr.base?.ref !== "main" || !newName ||
      pr.head?.repo?.full_name !== fullName ||
      oldName === context.payload.repository?.default_branch) {
    core.info("跳过：只处理本仓库已合并至 main 的 V<主版本>.<小版本> 分支。");
    return { status: "skipped" };
  }
  const repo = context.repo;
  async function getRef(name) {
    try {
      return (await github.rest.git.getRef({ ...repo, ref: `heads/${name}` })).data;
    } catch (error) {
      if (error.status === 404) return null;
      throw error;
    }
  }
  async function descendsFrom(base, head) {
    if (base === head) return true;
    const comparison = await github.rest.repos.compareCommitsWithBasehead({ ...repo, basehead: `${base}...${head}` });
    return ["ahead", "identical"].includes(comparison.data.status);
  }
  async function finish(status, note) {
    core.setOutput("old_branch", oldName);
    core.setOutput("new_branch", newName);
    await core.summary.addHeading("版本开发分支更新")
      .addTable([["原分支", "新分支", "结果"], [oldName, newName, note]])
      .write();
    return { status, oldBranch: oldName, newBranch: newName };
  }
  const source = await getRef(oldName);
  const target = await getRef(newName);
  if (target) {
    // 重试已完成的事件时不再递增；现存的其他目标分支不得覆盖。
    if (!source && await descendsFrom(pr.head.sha, target.object.sha)) {
      return finish("already-current", "已经完成，保留现有分支");
    }
    throw new Error(`目标 ${newName} 已存在，停止操作并保留两个分支。`);
  }
  const main = await getRef("main");
  if (!main) throw new Error("main 分支不存在，停止操作。");
  if (!source) {
    // GitHub 自动删除源分支时，从已合并的稳定分支建立下一开发分支。
    await github.rest.git.createRef({ ...repo, ref: `refs/heads/${newName}`, sha: main.object.sha });
    return finish("created", "源分支已删除，新开发分支从 main 建立");
  }
  await github.rest.repos.renameBranch({ ...repo, branch: oldName, new_name: newName });
  // 更名在 GitHub 后台完成，等新引用可读后再尝试快进。
  let renamed;
  for (let attempt = 0; attempt < 5; attempt++) {
    renamed = await getRef(newName);
    if (renamed) break;
    await wait(1000);
  }
  if (!renamed) throw new Error(`GitHub 已接受更名，但 ${newName} 尚不可读；稍后重试本次运行。`);
  if (await descendsFrom(source.object.sha, main.object.sha)) {
    // 只做快进，不覆盖分支重命名期间到达的新提交。
    try {
      await github.rest.git.updateRef({ ...repo, ref: `heads/${newName}`, sha: main.object.sha, force: false });
    } catch (error) {
      if (error.status !== 422) throw error;
      core.warning("分支已更名；未能快进到 main，保留并发提交及当前历史。");
      return finish("renamed", "已更名，保留并发提交及当前历史");
    }
    return finish("renamed", "已更名并快进到 main");
  }
  // squash/rebase 合并或源分支继续开发时，保留原提交，不强推重置。
  return finish("renamed", "已更名，保留原提交；未强制同步 main");
}

module.exports = { nextVersion, advanceVersionBranch };
