# 🔧 Jira Deployment Integration Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Issue 1: Deployments Not Showing in Jira

**Root Causes:**
1. **Missing GitHub Secrets**
2. **Incorrect Jira Configuration**
3. **Jira Permissions Issues**
4. **Integration Not Enabled**

---

## ✅ **Step-by-Step Fix**

### 1. **Set Up GitHub Secrets** (Required)

Go to: `https://github.com/AseshNemal/DailyMuse/settings/secrets/actions`

Add these secrets:

```
Name: JIRA_URL
Value: https://aseshnemal.atlassian.net

Name: JIRA_EMAIL
Value: aseshnemal@gmail.com

Name: JIRA_API_TOKEN  
Value: [Get from: https://id.atlassian.com/manage-profile/security/api-tokens]
```

### 2. **Enable Jira Development Integration**

#### A. In Your Jira Project:
1. Go to: `https://aseshnemal.atlassian.net/jira/settings/apps`
2. Find **"GitHub for Jira"** app
3. Click **"Get it now"** if not installed
4. Configure the connection:
   - Link your GitHub account
   - Select repositories to connect

#### B. Alternative - Manual Integration:
1. Go to: `https://aseshnemal.atlassian.net/plugins/servlet/applications/versions`
2. Click **"Link application"**
3. Choose **GitHub**
4. Follow the setup wizard

### 3. **Fix Common Permission Issues**

#### A. Jira API Token Permissions:
- Token must have **Read/Write** access
- User must be **Project Administrator** or have **Development** permissions

#### B. GitHub Repository Settings:
1. Go to: `Settings → Actions → General`
2. Set **Workflow permissions** to: `Read and write permissions`
3. Enable: `Allow GitHub Actions to create and approve pull requests`

---

## 🧪 **Test the Integration**

### Quick Test Method:

1. **Make a small change:**
   ```bash
   echo "Test deployment $(date)" >> test-deployment.txt
   git add test-deployment.txt
   git commit -m "PID-8: Test deployment integration"
   git push origin feature/PID-8-automated-medium-posting
   ```

2. **Check Results:**
   - ✅ GitHub Actions: https://github.com/AseshNemal/DailyMuse/actions
   - ✅ Jira Issue: https://aseshnemal.atlassian.net/browse/PID-8

---

## 🔍 **Debugging Steps**

### 1. **Check GitHub Actions Logs**
- Go to: Actions → Latest workflow run
- Look for errors in:
  - "Login to Jira" step
  - "Update Jira issue" step
  - "Send Jira deployment webhook" step

### 2. **Common Error Messages & Fixes**

#### ❌ "Authentication failed"
**Fix:** Regenerate Jira API token
1. https://id.atlassian.com/manage-profile/security/api-tokens
2. Delete old token
3. Create new token
4. Update GitHub secret `JIRA_API_TOKEN`

#### ❌ "Issue does not exist"
**Fix:** Check branch name format
- ✅ Correct: `feature/PID-8-description`
- ❌ Wrong: `feature/pid-8-description` (lowercase)
- ❌ Wrong: `feature/description-only`

#### ❌ "Forbidden" or "Permission denied"
**Fix:** Check Jira permissions
1. Go to Jira project settings
2. Permissions → Development
3. Ensure your user can "View/Create deployments"

### 3. **Manual Test API Connection**

Test your Jira API credentials:

```bash
curl -u "aseshnemal@gmail.com:YOUR_API_TOKEN" \
  -H "Accept: application/json" \
  "https://aseshnemal.atlassian.net/rest/api/2/issue/PID-8"
```

Should return issue details if working.

---

## 🎯 **Alternative Solutions**

### Option 1: **Use GitHub Integration App**
1. Install: https://github.com/marketplace/jira-software-github
2. Connect repositories automatically
3. Deployments will show without workflow changes

### Option 2: **Simplified Workflow**
If complex deployment tracking fails, use comment-only approach:

```yaml
- name: Simple Jira Update
  run: |
    curl -u "${{ secrets.JIRA_EMAIL }}:${{ secrets.JIRA_API_TOKEN }}" \
      -X POST \
      -H "Content-Type: application/json" \
      -d '{"body": "🚀 Deployed: ${{ github.ref_name }} at $(date)"}' \
      "${{ secrets.JIRA_URL }}/rest/api/2/issue/PID-8/comment"
```

### Option 3: **Manual Deployment Timeline**
1. Go to PID-8 in Jira
2. Click **"Deployments"** tab
3. Click **"Link deployment"**
4. Manually add GitHub Actions run URL

---

## 📋 **Verification Checklist**

After setup, verify:

- [ ] ✅ GitHub secrets are set correctly
- [ ] ✅ Jira API token has proper permissions  
- [ ] ✅ Branch name contains valid issue key (PID-8)
- [ ] ✅ GitHub Actions workflow runs without errors
- [ ] ✅ Jira issue shows comment from GitHub Actions
- [ ] ✅ Jira deployment timeline shows entries
- [ ] ✅ Links between GitHub and Jira work both ways

---

## 🆘 **Still Not Working?**

### Debug Commands:

1. **Check workflow logs:**
   ```bash
   # View latest workflow
   gh run list --repo AseshNemal/DailyMuse
   gh run view --repo AseshNemal/DailyMuse [RUN_ID]
   ```

2. **Test Jira API directly:**
   ```bash
   # Test authentication
   curl -u "email:token" https://aseshnemal.atlassian.net/rest/api/2/myself
   
   # Test issue access
   curl -u "email:token" https://aseshnemal.atlassian.net/rest/api/2/issue/PID-8
   ```

3. **Verify issue key extraction:**
   ```bash
   echo "feature/PID-8-automated-medium-posting" | grep -oE '[A-Z]+-[0-9]+'
   # Should output: PID-8
   ```

---

## 📞 **Need More Help?**

**Common Support Resources:**
- Jira API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v2/
- GitHub Actions Docs: https://docs.github.com/en/actions
- Atlassian Community: https://community.atlassian.com/

**Quick Fixes to Try:**
1. Regenerate all API tokens
2. Re-install GitHub for Jira app
3. Use simpler comment-only integration
4. Check Jira project permissions manually

The key is getting the basic GitHub → Jira comment working first, then adding deployment features once the connection is stable! 🚀
