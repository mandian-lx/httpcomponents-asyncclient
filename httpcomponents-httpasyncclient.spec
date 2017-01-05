Name:          httpcomponents-asyncclient
Version:       4.1.2
Release:       1
Summary:       Apache components to build asynchronous client side HTTP services
License:       ASL 2.0
URL:           http://hc.apache.org/
Source0:       http://www.apache.org/dist/httpcomponents/httpasyncclient/source/%{name}-%{version}-src.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.httpcomponents:httpclient-cache)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
BuildRequires: mvn(org.apache.httpcomponents:httpcore)
BuildRequires: mvn(org.apache.httpcomponents:httpcore-nio)
BuildRequires: mvn(org.apache.httpcomponents:project:pom:)
BuildRequires: mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires: mvn(org.mockito:mockito-core)

BuildArch:     noarch

%description
Asynch HttpClient is a HTTP/1.1 compliant HTTP agent implementation based on
HttpCore NIO and HttpClient components. It is a complementary module to
Apache HttpClient intended for special cases where ability to handle
a great number of concurrent connections is more important than performance
in terms of a raw data throughput.

%package cache
Summary:       Apache HttpAsyncClient Cache

%description cache
This package provides client side caching for %{name}.

%package parent
Summary:       Apache HttpAsyncClient Parent POM

%description parent
Apache HttpAsyncClient Parent POM.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
# Cleanup
find . -name "*.class" -delete
find . -name "*.jar" -type f -delete

# Use unavalable org.apache.httpcomponents:hc-stylecheck:jar:1
%pom_remove_plugin :maven-checkstyle-plugin
# Unwanted
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-source-plugin
# Unavalable
%pom_remove_plugin :clirr-maven-plugin

%pom_disable_module httpasyncclient-osgi

# Prevent build failure
%pom_remove_plugin -r :apache-rat-plugin

# Unavalable test deps: org.easymock:easymockclassextension org.apache.httpcomponents:httpclient-cache:test-jar
%pom_xpath_remove "pom:dependency[pom:type = 'test-jar']" httpasyncclient-cache
%pom_xpath_remove "pom:dependency[pom:scope = 'test']" httpasyncclient-cache
rm -r httpasyncclient-cache/src/test/java

# Add OSGi support
for p in httpasyncclient httpasyncclient-cache; do
 %pom_xpath_set "pom:project/pom:packaging" bundle ${p}
 %pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 ${p} "
 <extensions>true</extensions>
 <configuration>
  <instructions>
    <Export-Package>*</Export-Package>
  </instructions>
  <excludeDependencies>true</excludeDependencies>
 </configuration>"
done

%mvn_file org.apache.httpcomponents:httpasyncclient httpasyncclient
%mvn_file org.apache.httpcomponents:httpasyncclient-cache httpasyncclient-cache

%build

%mvn_build -s -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles-httpasyncclient
%doc README.txt RELEASE_NOTES.txt
%doc LICENSE.txt NOTICE.txt

%files cache -f .mfiles-httpasyncclient-cache
%doc LICENSE.txt NOTICE.txt

%files parent -f .mfiles-%{name}
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Sat Sep 10 2016 gil cattaneo <puntogil@libero.it> 4.1.2-1
- update to 4.1.2

* Fri Jun 24 2016 gil cattaneo <puntogil@libero.it> 4.1.1-4
- remove deprecated httpclient annotations

* Mon Jun 20 2016 gil cattaneo <puntogil@libero.it> 4.1.1-3
- add missing build requires: maven-plugin-bundle

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 gil cattaneo <puntogil@libero.it> 4.1.1-1
- update to 4.1.1

* Sun Jul 26 2015 gil cattaneo <puntogil@libero.it> 4.1-2
- add, also for cache sub-package, license and notice files

* Sun May 24 2015 gil cattaneo <puntogil@libero.it> 4.1-1
- initial rpm


