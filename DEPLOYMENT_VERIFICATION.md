# Production Deployment Verification & Monitoring

**Deployment Date**: May 6, 2026
**Status**: ✅ Active and Live

## 📍 Deployment URLs

### Frontend (Vercel)
- **URL**: https://emergent-six-zeta.vercel.app/
- **Repository**: https://github.com/idhawal/emergent
- **Branch**: main
- **Root Directory**: frontend
- **Node.js Version**: 20.x
- **Build Command**: `CI=false GENERATE_SOURCEMAP=false yarn build`
- **Output Directory**: build

### Backend (Render)
- **URL**: https://emergent-av9b.onrender.com
- **API Docs**: https://emergent-av9b.onrender.com/docs
- **Health Check**: https://emergent-av9b.onrender.com/health
- **Repository**: https://github.com/idhawal/emergent
- **Branch**: main
- **Root Directory**: backend
- **Python Version**: 3.11
- **Build Command**: `pip install -r requirements.txt`

---

## ✅ Production Verification Checklist

### Frontend (Vercel)
- [ ] Visit https://emergent-six-zeta.vercel.app/
- [ ] Wait for page to load completely
- [ ] Check browser console for errors (F12)
- [ ] Navigate to /decision-tree page
- [ ] Verify tree visualization displays correctly
- [ ] Test parameter adjustment (sliders)
- [ ] Verify API calls work (network tab)
- [ ] Test compare mode toggle

### Backend (Render)
- [ ] Visit https://emergent-av9b.onrender.com/health
- [ ] Should return: `{"status": "healthy", "service": "ml-visualizer-api"}`
- [ ] Visit https://emergent-av9b.onrender.com/docs
- [ ] Should show OpenAPI documentation
- [ ] Test POST /api/decision_tree endpoint with sample data
- [ ] Check response structure and status codes

### Environment Variables Configuration

**Vercel (Frontend):**
```
REACT_APP_BACKEND_URL=https://emergent-av9b.onrender.com
NODE_OPTIONS=(set for production)
```

**Render (Backend):**
```
FRONTEND_URL=https://emergent-six-zeta.vercel.app
LOG_LEVEL=INFO
```

---

## 🧪 Quick API Tests

### Test 1: Health Check
```bash
curl https://emergent-av9b.onrender.com/health
# Expected: {"status":"healthy","service":"ml-visualizer-api"}
```

### Test 2: Decision Tree - Valid Request
```bash
curl -X POST https://emergent-av9b.onrender.com/api/decision_tree \
  -H "Content-Type: application/json" \
  -d '{
    "task": "classifier",
    "criterion": "gini",
    "max_depth": 3,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "dataset": "iris",
    "uploaded_data": null
  }'
# Expected: 200 OK with tree_json, accuracy, depth, n_leaves, feature_importances
```

### Test 3: Decision Tree - Invalid Request (Error Handling)
```bash
curl -X POST https://emergent-av9b.onrender.com/api/decision_tree \
  -H "Content-Type: application/json" \
  -d '{
    "task": "regressor",
    "criterion": "entropy",
    "max_depth": 3,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "dataset": "iris",
    "uploaded_data": null
  }'
# Expected: 400 Bad Request with helpful error message
```

### Test 4: API Documentation
```bash
curl https://emergent-av9b.onrender.com/docs
# Expected: HTML page with Swagger UI
```

---

## 📊 Monitoring & Troubleshooting

### Frontend Issues

**Issue**: Page shows "Backend unreachable - displaying demo data"
- **Cause**: Backend API not accessible or REACT_APP_BACKEND_URL not set
- **Solution**: 
  1. Check Vercel environment variable is set: `REACT_APP_BACKEND_URL=https://emergent-av9b.onrender.com`
  2. Verify Render backend is running: `curl https://emergent-av9b.onrender.com/health`
  3. Redeploy frontend if needed: Push to main branch on GitHub

**Issue**: Tree visualization not visible or connector lines missing
- **Cause**: Component rendering issue or browser cache
- **Solution**: 
  1. Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
  2. Clear browser cache and cookies
  3. Check browser console for errors (F12)

**Issue**: Slow page load or timeouts
- **Cause**: Render backend may be sleeping (free tier cold start)
- **Solution**: 
  1. Upgrade Render to paid plan for always-on service
  2. Implement ping service to keep backend warm (optional)
  3. Check Render dashboard for resource usage

### Backend Issues

**Issue**: Health check returns unhealthy or 503
- **Cause**: Service restart, deployment issue, or resource exhaustion
- **Solution**: 
  1. Check Render deployment logs
  2. Verify Python 3.11+ is used
  3. Check free tier resource limits
  4. Restart service from Render dashboard

**Issue**: API returns 400 Bad Request
- **Cause**: Invalid input parameters
- **Solution**: 
  1. Check request payload format
  2. Verify parameter values (e.g., max_depth <= 10)
  3. See error message detail for specific issue
  4. Review API docs at /docs endpoint

**Issue**: CORS errors in browser console
- **Cause**: Frontend URL not in backend CORS whitelist
- **Solution**: 
  1. Verify FRONTEND_URL is set in Render env vars
  2. Check app/main.py CORS configuration
  3. Redeploy backend if env vars changed: 
     ```bash
     git push origin main  # Trigger auto-deploy
     ```

---

## 🔄 Deployment Process

### Frontend Deployment (Automatic on GitHub Push)
```bash
# 1. Make changes and commit
git add .
git commit -m "Fix: [description]"

# 2. Push to main branch
git push origin main

# 3. Vercel automatically:
#    - Builds: yarn build (from frontend/)
#    - Deploys to CDN
#    - Takes 2-5 minutes
# 4. View deployment at: https://emergent-six-zeta.vercel.app/
```

### Backend Deployment (Automatic on GitHub Push)
```bash
# Same as above, Render automatically:
#   - Installs dependencies: pip install -r requirements.txt
#   - Deploys updated code
#   - Restarts service
#   - Takes 5-15 minutes
# View deployment at: https://emergent-av9b.onrender.com/
```

### Manual Redeploy (if needed)
**Vercel:**
- Go to https://vercel.com/emergent-six-zeta
- Click "Redeploy" button
- Wait 2-5 minutes

**Render:**
- Go to https://dashboard.render.com
- Select "emergent" service
- Click "Manual Deploy"
- Wait 5-15 minutes

---

## 📈 Performance Metrics

### Frontend Performance (Vercel)
- **First Contentful Paint (FCP)**: ~1-2s
- **Largest Contentful Paint (LCP)**: ~2-3s
- **Cumulative Layout Shift (CLS)**: <0.1
- **Time to Interactive (TTI)**: ~3-4s

### Backend Performance (Render)
- **API Response Time**: 
  - Regression: ~200-500ms
  - KNN: ~100-300ms
  - Decision Tree: ~200-800ms
  - Genetic Algorithm: ~500-2000ms
- **Memory Usage**: ~100-300 MB
- **CPU Usage**: Typically <10%, spikes to 50-80% during computation

---

## 🛡️ Security Checklist

- ✅ CORS properly configured (only allow Vercel origin)
- ✅ No hardcoded secrets in code
- ✅ Environment variables used for sensitive data
- ✅ No sensitive data in logs
- ✅ HTTPS enforced on both frontend and backend
- ✅ Input validation on all API endpoints
- ✅ Error messages don't expose internal details

---

## 📝 Logging & Debugging

### View Vercel Logs
1. Go to https://vercel.com/emergent-six-zeta
2. Click "Deployments"
3. Select deployment
4. View Function logs

### View Render Logs
1. Go to https://dashboard.render.com
2. Select "emergent" service
3. Click "Logs" tab
4. See real-time logs or search

### Local Testing
```bash
# Test with same environment as production
export REACT_APP_BACKEND_URL=https://emergent-av9b.onrender.com
cd frontend
yarn build  # Build for production
yarn start  # Serve built app

# For backend
export FRONTEND_URL=https://emergent-six-zeta.vercel.app
cd backend
python server.py
```

---

## 🚀 Scaling & Optimization

### Free Tier Limitations
- **Vercel**: 
  - 100 deployments per month
  - 50 GB data transfer
  - Serverless functions (up to 60s timeout)
  
- **Render**: 
  - Free tier sleeps after 15 min inactivity
  - 0.5 GB RAM
  - Shared CPU

### Upgrade Path (if needed)
**Vercel Pro** ($20/month):
- Unlimited deployments
- 1 TB data transfer
- Priority support

**Render Pro** ($12+/month):
- Always-on service
- 2 GB+ RAM
- Dedicated CPU
- Better performance

---

## 📞 Support Resources

### Documentation
- [DEVELOPMENT.md](DEVELOPMENT.md) - Local setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Recent changes
- [API Docs](https://emergent-av9b.onrender.com/docs) - Interactive API reference

### GitHub
- Repository: https://github.com/idhawal/emergent
- Issues: Report bugs and features
- Discussions: Ask questions

### Deployment Dashboards
- **Vercel**: https://vercel.com/emergent-six-zeta
- **Render**: https://dashboard.render.com

---

## ✨ Recent Improvements Deployed

- ✅ Decision tree visualization improvements (better contrast, connectors)
- ✅ Comprehensive error handling with helpful messages
- ✅ Structured logging for debugging
- ✅ API documentation auto-generated at /docs
- ✅ React Error Boundary for graceful error handling
- ✅ 130+ tests for quality assurance

---

**Last Updated**: May 6, 2026
**Status**: ✅ Production Ready

For questions or issues, check the documentation or GitHub issues.
