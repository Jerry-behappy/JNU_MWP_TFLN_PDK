// 时间: 2026-10
// 使用内存 API 验证引用变更，测试不连接 GitHub、不修改真实分支。
"use strict";
const assert = require("node:assert/strict");
const { test } = require("node:test");
const { nextVersion, advanceVersionBranch } = require("./advance_version_branch.js");

function fixture(options = {}) {
  const refs = new Map(Object.entries(options.refs || { main: "merged", "V1.4": "pr-head" }));
  const writes = [], outputs = {}, warnings = [], calls = [];
  let renamed = false, delay = options.delay || 0;
  const context = {
    repo: { owner: "owner", repo: "pdk" },
    payload: {
      repository: { default_branch: "main" },
      pull_request: { merged: true, base: { ref: "main" }, head: { ref: "V1.4", sha: "pr-head", repo: { full_name: "owner/pdk" } } },
    },
  };
  const summary = { addHeading() { return this; }, addTable() { return this; }, async write() {} };
  const core = { info() {}, warning(value) { warnings.push(value); }, setOutput(k, v) { outputs[k] = v; }, summary };
  const github = { rest: {
    git: {
      async getRef(args) {
        calls.push(args);
        if (options.forbidden) throw Object.assign(new Error("forbidden"), { status: 403 });
        const name = args.ref.replace(/^heads\//, "");
        if ((renamed && name === "V1.5" && delay-- > 0) || !refs.has(name)) {
          throw Object.assign(new Error("not found"), { status: 404 });
        }
        return { data: { object: { sha: refs.get(name) } } };
      },
      async createRef(args) {
        writes.push({ operation: "create", ...args });
        refs.set(args.ref.replace(/^refs\/heads\//, ""), args.sha);
      },
      async updateRef(args) {
        writes.push({ operation: "update", ...args });
        const name = args.ref.replace(/^heads\//, "");
        if (options.concurrent) {
          refs.set(name, "new-work");
          throw Object.assign(new Error("not fast forward"), { status: 422 });
        }
        refs.set(name, args.sha);
      },
    },
    repos: {
      async renameBranch(args) {
        writes.push({ operation: "rename", ...args });
        refs.set(args.new_name, refs.get(args.branch));
        refs.delete(args.branch);
        renamed = true;
      },
      async compareCommitsWithBasehead(args) {
        calls.push(args);
        return { data: { status: options.diverged ? "diverged" : "ahead" } };
      },
    },
  } };
  const run = () => advanceVersionBranch({ github, context, core, wait: async () => {} });
  return { refs, writes, outputs, warnings, calls, context, run };
}

test("小版本按整数递增，不按小数进位", () => {
  assert.equal(nextVersion("V1.4"), "V1.5");
  assert.equal(nextVersion("V1.9"), "V1.10");
  assert.equal(nextVersion("V0.0"), "V0.1");
  assert.equal(nextVersion("V12.99999999999999999999"), "V12.100000000000000000000");
  for (const name of ["main", "ci/setup", "V1", "V01.4", "V1.4/other", "v1.4", "V1.4.1", undefined]) assert.equal(nextVersion(name), null);
});

test("未合并、其他基准、fork、普通分支和默认分支不触碰引用", async () => {
  for (const change of [
    f => { f.context.payload.pull_request.merged = false; },
    f => { f.context.payload.pull_request.base.ref = "other"; },
    f => { f.context.payload.pull_request.head.repo.full_name = "fork/pdk"; },
    f => { f.context.payload.pull_request.head.ref = "ci/setup"; },
    f => { f.context.payload.repository.default_branch = "V1.4"; },
  ]) {
    const f = fixture(); change(f);
    assert.equal((await f.run()).status, "skipped");
    assert.equal(f.calls.length, 0); assert.equal(f.writes.length, 0);
  }
});

test("合并后真正更名并只做快进，重试不再次递增", async () => {
  const f = fixture({ delay: 2 });
  assert.equal((await f.run()).status, "renamed");
  assert.equal(f.refs.has("V1.4"), false);
  assert.equal(f.refs.get("V1.5"), "merged");
  assert.deepEqual(f.writes.map(x => x.operation), ["rename", "update"]);
  assert.equal(f.writes[1].force, false);
  assert.equal(f.outputs.new_branch, "V1.5");
  assert.equal((await f.run()).status, "already-current");
  assert.equal(f.writes.length, 2);
});

test("已有目标分支不得覆盖", async () => {
  const f = fixture({ refs: { main: "merged", "V1.4": "pr-head", "V1.5": "other-work" } });
  await assert.rejects(f.run, /已存在/);
  assert.equal(f.refs.get("V1.5"), "other-work");
  assert.equal(f.refs.get("V1.4"), "pr-head");
  assert.equal(f.writes.length, 0);
});

test("源分支自动删除后，从 main 建立下一版本", async () => {
  const f = fixture({ refs: { main: "merged" } });
  assert.equal((await f.run()).status, "created");
  assert.equal(f.refs.get("V1.5"), "merged");
  assert.deepEqual(f.writes.map(x => x.operation), ["create"]);
});

test("squash/rebase 或后续开发的分叉历史保持不变", async () => {
  const f = fixture({ diverged: true });
  assert.equal((await f.run()).status, "renamed");
  assert.equal(f.refs.get("V1.5"), "pr-head");
  assert.deepEqual(f.writes.map(x => x.operation), ["rename"]);
});

test("快进时发生并发提交，保留新提交并报告", async () => {
  const f = fixture({ concurrent: true });
  assert.equal((await f.run()).status, "renamed");
  assert.equal(f.refs.get("V1.5"), "new-work");
  assert.equal(f.warnings.length, 1);
  assert.equal(f.writes[1].force, false);
});

test("权限错误不伪装成源分支缺失", async () => {
  const f = fixture({ forbidden: true });
  await assert.rejects(f.run, /forbidden/);
  assert.equal(f.writes.length, 0);
});
