import (
	"context"
	"log"
	"net/http"
	"time"
)

type Instance struct {
	db *badger.DB

	httpServer *http.Server
}

func NewInstance() *Instance {
	s := &Instance{
		// just in case you need some setup here
	}

	return s
}

func (s *Instance) Start() {

	// Startup all dependencies
	// I usually panic if any essential like the DB fails
	// e.g. due to wrong configurations
	s.db = MustOpenDb(dataDir)
	defer s.closeDb()

	// Startup the http Server in a way that
	// we can gracefully shut it down again
	s.httpServer = &http.Server{Addr: addr, Handler: endpoints.Router}
	err = s.httpServer.ListenAndServe() // Blocks!

	if err != http.ErrServerClosed {
		logrus.WithError(err).Error("Http Server stopped unexpected")
		s.Shutdown()
	} else {
		logrus.WithError(err).Info("Http Server stopped")
	}
}

func (s *Instance) Shutdown() {
	if s.httpServer != nil {
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		err := s.httpServer.Shutdown(ctx)
		if err != nil {
			logrus.WithError(err).Error("Failed to shutdown http server gracefully")
		} else {
			s.httpServer = nil
		}
	}
}

var Router = chi.NewRouter()

func SetupRoutes() {
	Router.Group(func(r chi.Router) {
		r.Use(apphandler.WithTypedContext)
		r.Use(apphandler.WithSession)
		r.Use(apphandler.WithTokenStore(TokenStore))
		r.Use(WithUser)

		InitIndex(r)
		InitAuth(r)
		InitDashboard(r)
		InitPlugins(r)
		InitUser(r)
		InitApi(r)
		r.Mount("/app/wiki", wiki.Router())
	})
}

// apphandler/context.go

type key int

const (
	userInfoKey key = iota
	sessionKey
	// ...
)

type Context struct {
	context.Context
}

func NewContext(ctx context.Context) Context {
	return Context{ctx}
}

func GetContext(r *http.Request) Context {
	if ctx, ok := r.Context().(Context); !ok {
		log.Panic("Failed to get custom Context from request")
		return ctx
	} else {
		return ctx
	}
}

func (ctx Context) WithUserInfo(userInfo UserInfo) Context {
	return Context{context.WithValue(ctx, userInfoKey, userInfo)}
}

func (ctx Context) UserInfo() UserInfo {
	val, ok := ctx.Value(userInfoKey).(UserInfo)
	if !ok {
		log.Panic("Failed to get UserInfo from context", val)
	}
	return val
}

// apphandler/middlewares.go

func WithTypedContext(next http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {

		ctx := NewContext(r.Context())
		r = r.WithContext(ctx)
		next.ServeHTTP(w, r)
	}
	return http.HandlerFunc(fn)
}

func WithUser(next http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		ctx := apphandler.GetContext(r)

		// Get everything you need, it's okay to use other depdendencies from ctx e.g. to access the session or database

		userInfo := apphandler.UserInfo{
			SessionId: sessionId,
			UserId:    userId,
		}

		ctx = ctx.WithUserInfo(userInfo)
		r = r.WithContext(ctx)
		next.ServeHTTP(w, r)
	}
	return http.HandlerFunc(fn)
}

if err != nil {
	response.Json(w, http.StatusInternalServerError, rest.NewErrorResponse(err))
	return
 }

 func appPageHandler(w http.ResponseWriter, r *http.Request) {
	page := applications.NewApplicationPage(r, appId)
 
	pages.RenderPage(w, page)
 }